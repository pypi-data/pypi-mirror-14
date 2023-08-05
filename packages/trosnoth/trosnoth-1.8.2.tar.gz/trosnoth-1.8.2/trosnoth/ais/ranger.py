import logging
from math import atan2, pi
import random

from twisted.internet import reactor

from trosnoth.ai import AI
from trosnoth.ais.pathfinding import NORTH, SOUTH, EAST, WEST, ORB
from trosnoth.messages import TickMsg
from trosnoth.utils import math, globaldebug
from trosnoth.utils.event import Event
from trosnoth.utils.twist import WeakLoopingCall

log = logging.getLogger(__name__)


SHOOTING = True


class RangerAI(AI):
    nick = 'RangerBot'
    playable = True

    def start(self):
        self.onTick = Event()
        self.recentGoals = {}
        self.clearRecent = None
        self.mainGoal = WinCurrentGame(self, None)

        self.mainGoal.start()

    def disable(self):
        self.mainGoal.stop()
        if self.clearRecent:
            self.clearRecent.cancel()
            self.clearRecent = None

    def showGoalStack(self):
        '''
        For debugging.
        '''
        log.error('Goal stack for %s:', self.player)
        curGoal = self.mainGoal
        while curGoal:
            log.error('  %s', curGoal)
            curGoal = curGoal.subGoal
        log.error('')

    def subGoalStopped(self, goal):
        # Record recent inactive goals so they can be reused if they come up
        # again.
        self.recentGoals[goal] = goal
        if self.clearRecent:
            self.clearRecent.cancel()
            self.clearRecent = None
        self.clearRecent = reactor.callLater(4, self.clearRecentGoals)

    def startingSubGoal(self, goal):
        if goal in self.recentGoals:
            del self.recentGoals[goal]

    def clearRecentGoals(self):
        self.clearRecent = None
        self.recentGoals.clear()

    def checkGoal(self, goal):
        result = self.recentGoals.get(goal, goal)
        result.parent = goal.parent
        return result

    @TickMsg.handler
    def handle_TickMsg(self, msg):
        self.onTick()

        if SHOOTING and self.player.canShoot():
            physics = self.world.physics
            gunRange = physics.shotLifetime * physics.shotSpeed
            shot = None
            for p in self.world.players:
                if p.dead or self.player.isFriendsWith(p):
                    continue
                if p.invisible or p.turret:
                    continue
                if math.distance(self.player.pos, p.pos) < gunRange:
                    # Check if we can shoot without hitting obstacles
                    if shot is None:
                        shot = self.player.createShot()
                    deltaX = p.pos[0] - self.player.pos[0]
                    deltaY = p.pos[1] - self.player.pos[1]
                    obstacle, dX, dY = physics.trimPathToObstacle(
                        shot, deltaX, deltaY, ())
                    if obstacle is None:
                        self.doAimAtPoint(p.pos)
                        self.doShoot()
                        return


class Goal(object):
    '''
    Represents something that the AI is trying to achieve.
    '''

    def __init__(self, ai, parent):
        self.ai = ai
        self.parent = parent
        self.subGoal = None

    def __str__(self):
        return self.__class__.__name__

    def start(self):
        '''
        Called when this goal should begin its work.
        '''
        self.reevaluate()

    def stop(self):
        '''
        Should disable any active components of this goal.
        '''
        if self.subGoal:
            self.subGoal.stop()
            self.subGoal = None

    def setSubGoal(self, goal):
        '''
        If the given goal is already the current sub-goal, does nothing.
        Otherwise, stops the current sub-goal, and starts the given one.
        '''
        if self.subGoal == goal:
            return
        if self.subGoal:
            self.subGoal.stop()
            self.subGoal.parent = None
            self.ai.subGoalStopped(goal)

        if goal:
            goal = self.ai.checkGoal(goal)
            self.subGoal = goal
            self.ai.startingSubGoal(goal)
            goal.start()
        else:
            self.subGoal = None

    def returnToParent(self):
        '''
        Call this method to tell the parent goal that this goal is either
        completed, or no longer relevant.
        '''
        if self.parent:
            reactor.callLater(0, self.parent.returnedFromChild, self)

    def returnedFromChild(self, child):
        '''
        Called by child's returnToParent() method. The default implementation
        checks that the returning child is this goal's subgoal, then calls
        reevaluate().
        '''
        if child is self.subGoal:
            self.reevaluate()
        else:
            self.ai.subGoalStopped(child)

    def reevaluate(self):
        '''
        Called by the default implementations of start() and
        returnedFromChild() to determine what this goal should do next.
        '''
        pass


class WinCurrentGame(Goal):
    def reevaluate(self):
        state = self.ai.world.state

        if not state.inMatch:
            # Lobby or similar
            self.setSubGoal(RunAroundKillingHumans(self.ai, self))
        elif state.isTrosball():
            self.setSubGoal(ScoreTrosballPoint(self.ai, self))
        elif state.becomeNeutralWhenDie():
            # Rabbit hunt
            self.setSubGoal(HuntTheRabbits(self.ai, self))
        else:
            self.setSubGoal(WinStandardTrosnothGame(self.ai, self))


class ScoreTrosballPoint(Goal):
    def reevaluate(self):
        if not self.ai.world.state.isTrosball():
            self.returnToParent()
            return

        # TODO: trosball logic
        self.setSubGoal(RunAroundKillingThings(self.ai, self))


class RunAroundKillingThings(Goal):
    def start(self):
        self.worldState = self.ai.world.state
        self.ai.world.onGameOver.addListener(self.reevaluate)
        self.ai.world.onReset.addListener(self.reevaluate)
        self.checkLoop = WeakLoopingCall(self, 'reevaluate')
        self.checkLoop.start(3)

    def stop(self):
        super(RunAroundKillingThings, self).stop()
        self.checkLoop.stop()
        self.ai.world.onGameOver.removeListener(self.reevaluate)
        self.ai.world.onReset.removeListener(self.reevaluate)

    def reevaluate(self):
        if self.ai.world.state != self.worldState:
            self.returnToParent()
            return

        player = self.ai.player

        if player.dead:
            zone = self.selectZone()
            if zone is None:
                zone = player.getZone()
                if zone is None:
                    zone = random.choice(list(self.ai.world.zones))
            self.setSubGoal(RespawnNearZone(self.ai, self, zone))
            return

        if player.getZone() and self.zoneIsOk(player.getZone()):
            # There are enemies here
            self.setSubGoal(MessAroundInZone(self.ai, self))
            return

        zone = self.selectZone()
        if zone:
            self.setSubGoal(MoveToOrbWhileAlive(self.ai, self, zone))
        else:
            self.setSubGoal(MessAroundInZone(self.ai, self))

    def zoneIsOk(self, zone):
        return any(
            (not p.dead and not self.ai.player.isFriendsWith(p))
            for p in zone.players)

    def selectZone(self):
        options = []
        for zone in self.ai.world.zones:
            if self.zoneIsOk(zone):
                options.append(zone)
        if not options:
            return None
        return random.choice(options)


class RunAroundKillingHumans(RunAroundKillingThings):
    def zoneIsOk(self, zone):
        return any(
            (not p.dead and not self.ai.player.isFriendsWith(p) and not p.bot)
            for p in zone.players)


class HuntTheRabbits(RunAroundKillingThings):
    def zoneIsOk(self, zone):
        return any(
            (
                not p.dead and not self.ai.player.isFriendsWith(p)
                and p.team is not None)
            for p in zone.players)


class WinStandardTrosnothGame(Goal):
    '''
    Win the current game of Trosnoth by capturing all the zones.
    '''

    def start(self):
        self.ai.world.onGameOver.addListener(self.reevaluate)
        self.ai.world.onReset.addListener(self.reevaluate)
        self.checkLoop = WeakLoopingCall(self, 'reevaluate')
        self.checkLoop.start(3)

    def stop(self):
        super(WinStandardTrosnothGame, self).stop()
        self.checkLoop.stop()
        self.ai.world.onGameOver.removeListener(self.reevaluate)
        self.ai.world.onReset.removeListener(self.reevaluate)

    def reevaluate(self, *args, **kwargs):
        '''
        Decide whether to stay in the current zone, or move to another.
        '''

        state = self.ai.world.state
        if (not state.inMatch) or state.becomeNeutralWhenDie():
            self.returnToParent()
            return

        player = self.ai.player
        myZone = player.getZone()

        # 1. If we're defending a disputed zone, stay in the zone
        if myZone and myZone.owner == player.team and myZone.isDisputed():
            self.setSubGoal(DefendZone(self.ai, self, myZone))
            return

        # 2. If we're attacking a capturable zone, stay in the zone
        if (
                myZone and myZone.owner != player.team
                and myZone.isCapturableBy(player.team)):
            self.setSubGoal(CaptureZone(self.ai, self, myZone))
            return

        # 3. Score other zones based on how helpful it would be to be there and
        #    how likely we are to get there in time.

        if player.dead:
            zone = self.getMostUrgentZone()
        else:
            zone = self.getMostLikelyUrgentZone(myZone)

        if zone is None:
            self.returnToParent()
        elif zone.owner == player.team:
            self.setSubGoal(DefendZone(self.ai, self, zone))
        else:
            self.setSubGoal(CaptureZone(self.ai, self, zone))

    def getMostUrgentZone(self):
        bestScore = 0
        bestOptions = []

        for zone in self.ai.world.zones:
            utility = self.getZoneUtility(zone)

            if not [
                    z for z in zone.getAdjacentZones()
                    if z.owner == zone.owner]:
                # This is the last remaining zone
                awesomeness = 5
            else:
                awesomeness = zone.consequenceOfCapture()

            score = utility * awesomeness
            if score == bestScore:
                bestOptions.append(zone)
            elif score > bestScore:
                bestOptions = [zone]
                bestScore = score

        if not bestOptions:
            return None

        return random.choice(bestOptions)

    def getMostLikelyUrgentZone(self, myZone):
        bestScore = 0
        bestOptions = []
        seen = {myZone}
        pending = [(zone, 0.7) for zone in myZone.getUnblockedNeighbours()]
        while pending:
            zone, likelihood = pending.pop(0)
            seen.add(zone)

            utility = self.getZoneUtility(zone)

            if not [
                    z for z in zone.getAdjacentZones()
                    if z.owner == zone.owner]:
                # This is the last remaining zone
                awesomeness = 5
            else:
                awesomeness = zone.consequenceOfCapture()

            score = likelihood * utility * awesomeness
            if score == bestScore:
                bestOptions.append(zone)
            elif score > bestScore:
                bestOptions = [zone]
                bestScore = score

            likelihood *= 0.7
            for other in zone.getUnblockedNeighbours():
                if other not in seen:
                    pending.append((other, likelihood))

        if not bestOptions:
            return None

        return random.choice(bestOptions)

    def getZoneUtility(self, zone):
        player = self.ai.player

        # Count the number of friendly players and players on the most
        # likely enemy team to tag the zone.
        enemy = friendly = 0
        for count, teams in zone.getPlayerCounts():
            if player.team in teams and not friendly:
                friendly = count
            if [t for t in teams if t != player.team] and not enemy:
                enemy = count
            if friendly and enemy:
                break

        if zone.owner == player.team:
            defence = min(3, friendly)
            if enemy == 0:
                utility = 0
            elif enemy > defence:
                # There's a slim chance you could shoot them before they
                # capture the zone.
                utility = 0.2 ** (enemy - defence)
            elif enemy == defence:
                # Being here will stop it being tagged
                utility = 1
            else:
                # There's a slim chance the enemy might shoot them
                utility = 0.2 ** (friendly - enemy)
        elif not zone.adjacentToAnotherZoneOwnedBy(player.team):
            # Cannot capture, have no adjacent zones
            utility = 0
        else:
            defence = min(3, enemy)
            if friendly > defence:
                # Already capturable, but there's a slim chance teammates
                # might die.
                utility = 0.2 ** (friendly - defence)
            elif friendly == defence:
                # Being here will enable the zone tag
                utility = 1
            else:
                # There's a slim chance you could shoot them and capture
                utility = 0.2 ** (friendly - enemy)
        return utility


class ZoneMixin(Goal):
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.zone == self.zone

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.zone)


class CaptureZone(ZoneMixin, Goal):
    '''
    Respawns if necessary, moves to the given zone, messes around until it's
    capturable, and captures it. If the player dies, respawns and tries again.
    Returns if the zone is captured or becomes uncapturable by virtue of having
    no adjacent zones owned by the team.
    '''

    def __init__(self, ai, parent, zone):
        super(CaptureZone, self).__init__(ai, parent)
        self.zone = zone

    def reevaluate(self):
        player = self.ai.player
        if self.zone.owner == player.team:
            self.returnToParent()
            return

        if not self.zone.adjacentToAnotherZoneOwnedBy(player.team):
            self.returnToParent()
            return

        if player.dead:
            self.setSubGoal(RespawnNearZone(self.ai, self, self.zone))
            return

        playerZone = player.getZone()
        if (
                playerZone == self.zone
                and not self.zone.isCapturableBy(player.team)):
            self.setSubGoal(MessAroundInZone(self.ai, self))
        else:
            self.setSubGoal(MoveToOrbWhileAlive(self.ai, self, self.zone))


class DefendZone(ZoneMixin, Goal):
    '''
    Respawns if necessary, moves to the given zone and messes around there.
    If the player dies, respawns and continues. Returns if the zone is
    captured or neutralised.
    '''

    def __init__(self, ai, parent, zone):
        super(DefendZone, self).__init__(ai, parent)
        self.zone = zone

    def reevaluate(self):
        player = self.ai.player
        if self.zone.owner != player.team:
            self.returnToParent()
            return

        if player.dead:
            self.setSubGoal(RespawnNearZone(self.ai, self, self.zone))
            return

        playerZone = player.getZone()
        if playerZone == self.zone:
            self.setSubGoal(MessAroundInZone(self.ai, self))
        else:
            self.setSubGoal(MoveToOrbWhileAlive(self.ai, self, self.zone))


class MessAroundInZone(Goal):
    '''
    Wander around in the zone the player is in at the time of construction.
    Mostly random, but has a slight tendency to move towards the orb.
    Aborts if the player dies or leaves the zone.
    '''

    def __init__(self, ai, parent):
        super(MessAroundInZone, self).__init__(ai, parent)
        self.zone = self.ai.player.getZone()
        self.action = None

    def start(self):
        self.ai.onTick.addListener(self.tick)
        super(MessAroundInZone, self).start()

    def stop(self):
        super(MessAroundInZone, self).stop()
        self.ai.onTick.removeListener(self.tick)

    def reevaluate(self):
        player = self.ai.player
        if player.dead:
            self.action = None
            self.returnToParent()
            return

        zone = player.getZone()
        if zone != self.zone:
            self.action = None
            self.returnToParent()
            return

        pathFinder = self.ai.world.map.layout.pathFinder
        if pathFinder is None:
            # Can't do anything without a path-finding database loaded
            self.action = None
            log.warning('No pathfinding database loaded')
            self.stop()
            return

        if random.random() < 0.1:
            # Move towards the orb
            block = player.getMapBlock()
            if block.defn.kind in ('top', 'btm'):
                self.action = pathFinder.getOrbAction(self.ai.player)
            elif block.defn.rect.centerx < zone.defn.pos[0]:
                self.action = pathFinder.getExitAction(self.ai.player, EAST)
            else:
                self.action = pathFinder.getExitAction(self.ai.player, WEST)
        else:
            # Move randomly
            self.action = random.choice(
                pathFinder.getAllActions(self.ai.player))

        if self.action is None:
            self.returnToParent()

    def tick(self):
        player = self.ai.player
        if player.dead:
            self.reevaluate()
            return

        if not self.action:
            self.reevaluate()
            if self.action is None:
                return

        done, stateChanges, faceRight = self.action.prepNextStep(player)

        if done:
            self.action = None
            return

        for key, value in stateChanges:
            self.ai._sendStateUpdate(key, value)

        if faceRight and not player.isFacingRight():
            self.ai.doAimAt(pi / 2)
        elif (not faceRight) and player.isFacingRight():
            self.ai.doAimAt(-pi / 2)


class RespawnNearZone(ZoneMixin, Goal):
    '''
    Respawns in a zone that's as close as possible to the given zone.
    '''

    def __init__(self, ai, parent, zone):
        super(RespawnNearZone, self).__init__(ai, parent)
        self.zone = zone

    def start(self):
        self.ai.world.onZoneTagged.addListener(self.zoneTagged)
        super(RespawnNearZone, self).start()

    def stop(self):
        super(RespawnNearZone, self).stop()
        self.ai.world.onZoneTagged.removeListener(self.zoneTagged)

    def zoneTagged(self, *args, **kwargs):
        '''
        We may be waiting to respawn in a zone that's just changed ownership.
        '''
        self.reevaluate()

    def reevaluate(self):
        player = self.ai.player
        if not player.dead:
            self.returnToParent()
            return

        bestZone = self.zone
        zones = [self.zone]
        seen = set()

        while zones:
            zone = zones.pop(0)
            seen.add(zone)
            if player.isZoneRespawnable(zone):
                bestZone = zone
                break
            adjacent = [
                z for z in zone.getUnblockedNeighbours() if z not in seen]
            random.shuffle(adjacent)
            zones.extend(adjacent)

        if player.getZone() == bestZone:
            self.setSubGoal(RespawnWhenPossible(self.ai, self))
        else:
            self.setSubGoal(MoveGhostToZone(self.ai, self, bestZone))


class MoveGhostToZone(ZoneMixin, Goal):
    def __init__(self, ai, parent, zone):
        super(MoveGhostToZone, self).__init__(ai, parent)
        self.zone = zone

    def start(self):
        self.ai.onTick.addListener(self.tick)

        zonePos = self.zone.defn.pos
        playerPos = self.ai.player.pos
        if zonePos == playerPos:
            return
        dx = zonePos[0] - playerPos[0]
        dy = zonePos[1] - playerPos[1]
        theta = atan2(dx, -dy)
        self.ai.doAimAt(theta, 1.0)

    def stop(self):
        super(MoveGhostToZone, self).stop()
        self.ai.onTick.removeListener(self.tick)

    def tick(self):
        if not self.ai.player.dead:
            self.returnToParent()
        elif self.ai.player.getZone() == self.zone:
            self.ai.doAimAt(0.0, 0.0)
            self.returnToParent()


class RespawnWhenPossible(Goal):
    def start(self):
        self.ai.onTick.addListener(self.tick)

    def stop(self):
        super(RespawnWhenPossible, self).stop()
        self.ai.onTick.removeListener(self.tick)

    def tick(self):
        player = self.ai.player
        if not (player.dead and player.inRespawnableZone()):
            # Impossible to respawn
            self.returnToParent()
            return

        if not player.world.abilities.respawn:
            return
        if player.respawnGauge > 0:
            return
        if player.getZone().frozen:
            return

        # Ready to respawn
        self.ai.doRespawn()


class MoveToOrbWhileAlive(ZoneMixin, Goal):

    def __init__(self, ai, parent, zone):
        super(MoveToOrbWhileAlive, self).__init__(ai, parent)
        self.zone = zone
        self.path = None

    def start(self):
        self.ai.onTick.addListener(self.tick)
        if __debug__ and globaldebug.enabled and globaldebug.showPathFinding:
            player = self.ai.world.getPlayer(self.ai.player.id)
            player.onOverlayDebugHook.addListener(self.overlay)

    def stop(self):
        super(MoveToOrbWhileAlive, self).stop()
        self.ai.onTick.removeListener(self.tick)
        if __debug__ and globaldebug.enabled and globaldebug.showPathFinding:
            player = self.ai.world.getPlayer(self.ai.player.id)
            player.onOverlayDebugHook.removeListener(self.overlay)

    def overlay(self, viewManager, screen, sprite):
        '''
        Shows debugging overlay. Enabled using flags in
        trosnoth.utils.globaldebug.
        '''
        if self.path is None or self.path.steps is None:
            return

        import pygame
        from trosnoth.trosnothgui.ingame.utils import mapPosToScreen
        focus = viewManager._focus
        area = viewManager.sRect
        prev = mapPosToScreen(sprite.pos, focus, area)
        for blockDef, scoreKey in self.path.steps:
            if blockDef is None:
                break
            if scoreKey == ORB:
                scoreKey = NORTH if blockDef.kind == 'btm' else SOUTH

            if scoreKey == NORTH:
                pt = mapPosToScreen(blockDef.rect.midtop, focus, area)
            elif scoreKey == SOUTH:
                pt = mapPosToScreen(blockDef.rect.midbottom, focus, area)
            elif scoreKey == EAST:
                pt = mapPosToScreen(blockDef.rect.midright, focus, area)
            elif scoreKey == WEST:
                pt = mapPosToScreen(blockDef.rect.midleft, focus, area)
            else:
                # Shouldn't happen
                pt = mapPosToScreen(blockDef.rect.centre)
            pygame.draw.line(screen, (255, 192, 0), prev, pt, 2)
            prev = pt

    def tick(self):
        player = self.ai.player

        if player.dead:
            self.returnToParent()
            return

        if self.path is None:
            pathFinder = self.ai.world.map.layout.pathFinder
            if pathFinder is None:
                # No path-finding database loaded
                log.warning('No pathfinding database loaded')
                self.stop()
                return

            self.path = pathFinder.getRouteToOrb(self.zone)
            # TODO: if the best path is more than a certain value, use bomber

        done, stateChanges, faceRight = self.path.prepNextStep(player)

        if done:
            self.path = None
            self.returnToParent()
            return

        for key, value in stateChanges:
            self.ai._sendStateUpdate(key, value)

        if faceRight and not player.isFacingRight():
            self.ai.doAimAt(pi / 2)
        elif (not faceRight) and player.isFacingRight():
            self.ai.doAimAt(-pi / 2)


AIClass = RangerAI
