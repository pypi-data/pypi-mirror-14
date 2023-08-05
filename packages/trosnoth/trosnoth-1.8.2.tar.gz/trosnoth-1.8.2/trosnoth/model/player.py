import copy
import logging
from math import sin, cos, pi, floor
import struct

from trosnoth.const import OFF_MAP_DEATH
from trosnoth.model.shot import Shot, PredictedGrenadeTrajectory
from trosnoth.model.trosball import PredictedTrosballTrajectory
from trosnoth.model.unit import Unit
from trosnoth.model.upgrades import Grenade
from trosnoth.utils.event import Event
from trosnoth.utils.math import distance, isNear

from trosnoth.messages import (
    PlayerUpdateMsg, ResyncPlayerMsg, ChatFromServerMsg, ResyncAcknowledgedMsg,
)

RESPAWN_CAMP_TIME = 1.0
MAX_STARS = 10
MAX_RESYNC_TIME = 4     # seconds

log = logging.getLogger('player')


class Player(Unit):
    '''Maintains the state of a player. This could be the user's player, a
    player on the network, or conceivably even a bot.
    '''

    HALF_WIDTH = 10
    HALF_HEIGHT = 19

    def __init__(
            self, world, nick, team, id, dead=False, bot=False,
            *args, **kwargs):
        super(Player, self).__init__(world, *args, **kwargs)

        self.world = world

        self.onDied = Event()       # (killer, deathType)
        self.onKilled = Event()     # (target, deathType)
        self.onZombieHit = Event()  # (killer, shot, deathType)
        self.onStarsChanged = Event()
        self.onNeutralisedSector = Event()  # (zoneCount)
        self.onTaggedZone = Event()         # (zone, previousOwner)
        self.onUsedUpgrade = Event()        # (upgrade)
        self.onAbandonUpgrade = Event()     # (upgrade)
        self.onUpgradeGone = Event()        # (upgrade)
        self.onShotFired = Event()          # (shot)
        self.onShotHurtPlayer = Event()     # (target, shot)
        self.onHitByShot = Event()          # (shot)
        self.onShieldDestroyed = Event()    # (shooter, deathType)
        self.onDestroyedShield = Event()    # (target, deathType)
        self.onPrivateChatReceived = Event()    # (text, sender)
        self.onGotTrosball = Event()
        self.onStarsSpent = Event()         # (stars)
        self.onRespawned = Event()
        self.onShotHitSomething = Event()   # (shot)
        self.onOverlayDebugHook = Event()   # (viewManager, screen, sprite)

        # Identity
        self.nick = nick
        self.user = None      # If authenticated, this will have a value.
        self.agent = None
        self.team = team
        self.id = id
        self.bot = bot

        # Preferences during the voting phase.
        self.preferredTeam = ''
        self.prefersTournamentTeam = False
        self.readyToStart = False
        self.readyForTournament = False
        self.preferredSize = (0, 0)
        self.preferredDuration = 0

        # Input state
        self._state = {'left':  False,
                       'right': False,
                       'jump':  False,
                       'down': False,
                       'respawn': False}

        # Physics
        self._alreadyJumped = False
        self._jumpTime = 0.0
        self.yVel = 0
        self.attachedObstacle = None
        self.motionState = 'fall'   # fall / ground / leftwall / rightwall
        self._unstickyWall = None
        self._ignore = None         # Used when dropping through a platform.
        self.angleFacing = 1.57
        self.ghostThrust = 0.0      # Determined by mouse position
        self._faceRight = True
        self.reloadTime = 0.0
        self.reloadFrom = 0.0
        self.turretHeat = 0.0
        self.respawnGauge = 0.0
        self.upgradeGauge = 0.0
        self.upgradeTotal = 0.0

        # Upgrade-related
        self.pendingUpgrade = None
        self.upgrade = None
        self.turretOverHeated = False
        self.invulnerableUntil = None
        self.mgBulletsRemaining = 0
        self.mgFiring = False

        # Other state info
        self.starsAtLastDeath = 0
        self.stars = world.PLAYER_RESET_STARS
        if dead:
            self.health = 0
        else:
            self.health = self.world.physics.playerRespawnHealth
        self.zombieHits = 0
        self.resyncing = False
        self.resyncExpiry = None

    def clone(self):
        '''
        Used to create the local representation of this player object.
        '''
        result = copy.copy(self)
        result._state = copy.copy(self._state)
        result.onDied = Event()
        result.onKilled = Event()
        result.onZombieHit = Event()
        result.onStarsChanged = Event()
        result.onNeutralisedSector = Event()
        result.onTaggedZone = Event()
        result.onUsedUpgrade = Event()
        result.onAbandonUpgrade = Event()
        result.onUpgradeGone = Event()
        result.onShotFired = Event()
        result.onShotHurtPlayer = Event()
        result.onHitByShot = Event()
        result.onShieldDestroyed = Event()
        result.onDestroyedShield = Event()
        result.onPrivateChatReceived = Event()
        result.onGotTrosball = Event()
        result.onStarsSpent = Event()
        result.onRespawned = Event()
        result.onShotHitSomething = Event()
        result.onOverlayDebugHook = Event()
        return result

    def dump(self):
        return {
            'id': self.id,
            'teamId': self.team.id if self.team else '\x00',
            'nick': self.nick,
            'bot': self.bot,
            'update': self.getPlayerUpdateArgs(),
            'upgrade':
                self.upgrade.upgradeType
                if self.upgrade else None,
            'upgradeTime': self.upgradeGauge,
            'preferences': {
                'team': self.preferredTeam,
                'tournament': self.prefersTournamentTeam,
                'size': self.preferredSize,
                'duration': self.preferredDuration,
                'ready': self.readyToStart,
                'readyForTournament': self.readyForTournament,
            }
        }

    def restore(self, data):
        team = self.world.teamWithId[data['teamId']]
        bot = data['bot']
        update = data['update']
        upgrade = data['upgrade']
        preferences = data['preferences']

        self.nick = data['nick']
        self.team = team
        self.bot = bot

        if self.upgrade and self.upgrade.upgradeType != upgrade:
            self.deleteUpgrade()
        if upgrade:
            if not self.upgrade or self.upgrade.upgradeType != upgrade:
                self.upgradeUsed(upgrade)
                self.upgradeGauge = data['upgradeTime']

        self.applyPlayerUpdate(PlayerUpdateMsg(*update))

        self.preferredTeam = preferences['team']
        self.preferredTournamentTeam = preferences['tournament']
        self.preferredSize = tuple(preferences['size'])
        self.preferredDuration = preferences['duration']
        self.readyToStart = preferences['ready']
        self.readyForTournament = preferences['readyForTournament']

    @property
    def dead(self):
        realHealth = self.health - self.zombieHits
        if self.hasProtectiveUpgrade():
            realHealth += self.upgrade.protections
        return realHealth <= 0

    @property
    def knowsItsDead(self):
        '''
        It's possible for a player to be dead and not know it (e.g. killed by
        grenade or shoxwave and hasn't yet received the network message). It
        this case the easiest way to keep the server and client in sync is by
        treating it as a ghost that moves like a living player.
        '''
        return self.health <= 0

    def isStatic(self):
        if self.oldPos != self.pos:
            return False
        if self.motionState == 'fall' and not self.knowsItsDead:
            return False
        if self.upgrade is not None:
            return False
        if self.knowsItsDead and self.respawnGauge != 0:
            return False
        if self.knowsItsDead and self.ghostThrust != 0:
            return False
        if self.reloadTime != 0:
            return False
        return True

    def getXKeyMotion(self):
        if self._state['left'] and not self._state['right']:
            return -1
        if self._state['right'] and not self._state['left']:
            return 1
        return 0

    def hasTrosball(self):
        return (
            self.world.trosballPlayer
            and self.world.trosballPlayer.id == self.id)

    @staticmethod
    def getObstacles(mapBlockDef):
        '''
        Return which obstacles in the given map block apply to this kind of
        unit.
        '''
        return mapBlockDef.obstacles + mapBlockDef.ledges

    @property
    def identifyingName(self):
        if self.user is None:
            return self.nick
        return self.user.username

    def hasProtectiveUpgrade(self):
        return self.upgrade is not None and self.upgrade.upgradeType in 'sd'

    def hasVisibleShield(self):
        if not self.hasProtectiveUpgrade():
            return False
        return self.upgrade.protections > self.zombieHits

    @property
    def phaseshift(self):
        return self.upgrade is not None and self.upgrade.upgradeType == 'h'

    @property
    def turret(self):
        return self.upgrade is not None and self.upgrade.upgradeType == 't'

    @property
    def shoxwave(self):
        return self.upgrade is not None and self.upgrade.upgradeType == 'w'

    @property
    def machineGunner(self):
        return self.upgrade is not None and self.upgrade.upgradeType in 'xd'

    @property
    def hasRicochet(self):
        return self.upgrade is not None and self.upgrade.upgradeType in 'rd'

    @property
    def ninja(self):
        return self.upgrade is not None and self.upgrade.upgradeType in 'nd'

    @property
    def disruptive(self):
        return self.upgrade is not None and self.upgrade.upgradeType == 'm'

    @property
    def bomber(self):
        return self.upgrade is not None and self.upgrade.upgradeType == 'b'

    @property
    def canMove(self):
        return not self.bomber

    @property
    def invisible(self):
        if self.ninja:
            if self.reloadTime != 0.0:
                return False
            if self.distanceFromCentre() > 200:
                return True
            zone = self.getZone()
            if zone and self.isFriendsWithTeam(zone.owner):
                return True
            return False
        return False

    @property
    def currentProjectileTrajectory(self):
        if self.dead:
            return None
        if self.hasTrosball():
            return PredictedTrosballTrajectory(self.world, self)
        if self.upgrade is not None:
            # Have an upgrade = cannot throw
            return None
        return PredictedGrenadeTrajectory(
            self.world, self, Grenade.timeRemaining)

    def distanceFromCentre(self):
        zone = self.getZone()
        if not zone:
            return 2000
        return distance(zone.defn.pos, self.pos)

    def isAttachedToWall(self):
        '''
        Returns False if this player is not attached to a wall, otherwise
        returns 'left' or 'right' to indicate whether the wall is on the
        player's left or right.
        '''
        if self.motionState == 'leftwall':
            return 'left'
        elif self.motionState == 'rightwall':
            return 'right'
        return False

    def detachFromEverything(self):
        self.setAttachedObstacle(None)

    def isOnGround(self):
        '''
        Returns True iff this player is on the ground (whether that ground is a
        ledge or solid ground).
        '''
        return self.motionState == 'ground'

    def isOnPlatform(self):
        return self.isOnGround() and self.attachedObstacle.drop

    def isFriendsWith(self, other):
        '''
        Returns True iff self and other are on the same team.
        '''
        if other.id == self.id:
            return True
        return self.isFriendsWithTeam(other.team)

    def isFriendsWithTeam(self, team):
        if team is None:
            return False
        return self.team == team

    def inRespawnableZone(self):
        zone = self.getZone()
        return self.isZoneRespawnable(zone)

    def isZoneRespawnable(self, zone):
        if not zone:
            return False
        return self.team is None or zone.owner == self.team

    @property
    def teamId(self):
        if self.team is None:
            return '\x00'
        return self.team.id

    @property
    def teamName(self):
        if self.team is None:
            return self.world.rogueTeamName
        return self.team.teamName

    def isEnemyTeam(self, team):
        '''
        Returns True iff the given team is an enemy team of this player. It is
        not enough for the team to be neutral (None), it must actually be an
        enemy for this method to return True.
        '''
        if team is None:
            return False
        return self.team != team

    def isInvulnerable(self):
        iu = self.invulnerableUntil
        if iu is None:
            return False
        elif self.world.timer.getElapsedTime() > iu:
            self.invulnerableUntil = None
            return False
        return True

    def getTeamStars(self):
        if self.team is None:
            return self.stars
        return self.world.getTeamStars(self.team)

    @property
    def isMinimapDisrupted(self):
        for team in self.world.teams:
            if team != self.team and team.usingMinimapDisruption:
                return True
        return False

    @staticmethod
    def _leftValidator(obs):
        return obs.deltaPt[0] == 0 and obs.deltaPt[1] > 0

    @staticmethod
    def _rightValidator(obs):
        return obs.deltaPt[0] == 0 and obs.deltaPt[1] < 0

    @staticmethod
    def _groundValidator(obs):
        return obs.deltaPt[0] > 0

    def setPos(self, pos, attached):
        self.pos = self.oldPos = pos

        self._ignore = None
        if attached == 'f':
            obstacle = None
        elif attached == 'g':
            obstacle, dX, dY = self.world.physics.trimPathToObstacle(
                self, 0, 10, set())
        elif attached == 'l':
            obstacle, dX, dY = self.world.physics.trimPathToObstacle(
                self, -10, 0, set())
        elif attached == 'r':
            obstacle, dX, dY = self.world.physics.trimPathToObstacle(
                self, 10, 0, set())
        self.setAttachedObstacle(obstacle)

    def __str__(self):
        return self.nick

    def getDetails(self):
        if self.id == -1:
            return {}

        pID = struct.unpack('B', self.id)[0]
        nick = self.nick
        team = self.teamId
        dead = self.dead
        stars = self.stars
        if self.upgrade:
            upgrade = str(self.upgrade)
        else:
            upgrade = None

        return {
            'pID': pID,
            'nick': nick,
            'team': team,
            'dead': dead,
            'stars': stars,
            'upgrade': upgrade,
            'bot': self.bot,
            'ready': self.readyToStart,
            'tournament': self.readyForTournament,
        }

    def removeFromGame(self):
        '''Called by network client when server says this player has left the
        game.'''

        if self.upgrade:
            self.upgrade.delete()

        if self.hasTrosball():
            self.world.trosballLost(self)

    def isSolid(self):
        return not self.knowsItsDead

    def ignoreObstacle(self, obstacle):
        return self._ignore == obstacle

    def continueOffMap(self):
        if not self.dead:
            # Player is off the map: mercy killing.
            self.killOutright(OFF_MAP_DEATH, resync=False)
        return False

    def canEnterZone(self, newZone):
        if newZone == self.getZone():
            return True
        world = self.world
        if (not world.abilities.leaveFriendlyZones
                and newZone is None and self.dead):
            # Pre-game ghost cannot enter purple zones.
            return False

        if (newZone is not None and
                not world.abilities.leaveFriendlyZones
                and newZone.owner != self.team):
            # Disallowed zone change.
            return False

        return True

    def updateState(self, key, value):
        '''Update the state of this player. State information is information
        which is needed to calculate the motion of the player. For a
        human-controlled player, this is essentially only which keys are
        pressed. Keys which define a player's state are: left, right, jump and
        down.
        Shooting is processed separately.'''

        if self.resyncing:
            return

        if key == 'left' or key == 'right':
            self._unstickyWall = None

        # Ignore messages if we already know the answer.
        if self._state[key] == value:
            return
        if key == 'jump':
            self._alreadyJumped = False

        # Set the state.
        self._state[key] = value

    def getState(self, key):
        return self._state[key]

    def processJumpState(self):
        '''
        Checks the player's jump key state to decide whether to initiate a jump
        or stop a jump.
        '''
        jumpKeyDown = self._state['jump'] and self.canMove
        if jumpKeyDown:
            if self.motionState == 'fall':
                return
            if self._alreadyJumped:
                return

            # Otherwise, initiate the jump.
            self._jumpTime = self.world.physics.playerMaxJumpTime
            if self.isAttachedToWall():
                self._unstickyWall = self.attachedObstacle
            self.detachFromEverything()
            self._alreadyJumped = True
        elif self._jumpTime > 0:
            # If we're jumping, cancel the jump.
            # The following line ensures that small jumps are possible
            #  while large jumps still curve.
            self.yVel = (
                -(1 - self._jumpTime / self.world.physics.playerMaxJumpTime)
                * self.world.physics.playerJumpThrust)
            self._jumpTime = 0

    def lookAt(self, angle, thrust=None):
        '''Changes the direction that the player is looking.  angle is in
        radians and is measured clockwise from vertical.'''

        if self.resyncing:
            return

        if thrust is not None:
            self.ghostThrust = min(1, max(0, thrust))

        angle = (angle + pi) % (2 * pi) - pi
        if self.angleFacing == angle:
            return

        self.angleFacing = angle
        self._faceRight = angle > 0

    def isFacingRight(self):
        return self._faceRight

    def upgradeUsed(self, upgradeType, local=None):
        upgradeKind = self.world.getUpgradeType(upgradeType)
        self.upgrade = upgradeKind(self)
        self.upgradeGauge = upgradeKind.timeRemaining
        self.upgradeTotal = upgradeKind.timeRemaining
        if local:
            self.upgrade.localUse(local)
        else:
            self.upgrade.use()
        self.onUsedUpgrade(self.upgrade)

    def checkUpgrades(self):
        # Update upgrade gauge based on Time:
        if self.upgrade and self.upgradeGauge > 0:
            self.upgradeGauge -= self.world.tickPeriod
            if self.upgradeGauge <= 0:
                self.upgrade.timeIsUp()
                self.deleteUpgrade()

    def updateGhost(self):
        deltaT = self.world.tickPeriod
        deltaX = (
            self.world.physics.playerMaxGhostVel * deltaT
            * sin(self.angleFacing) * self.ghostThrust)
        deltaY = (
            -self.world.physics.playerMaxGhostVel * deltaT
            * cos(self.angleFacing) * self.ghostThrust)

        self.world.physics.moveUnit(self, deltaX, deltaY)

        # Update respawn gauge based on Time:
        if self.respawnGauge >= 0:
            self.respawnGauge -= deltaT
            if self.respawnGauge < 0:
                self.respawnGauge = 0

    def updateTurret(self):
        deltaT = self.world.tickPeriod
        self.reloadTime = max(0.0, self.reloadTime - deltaT)
        self.turretHeat = max(0.0, self.turretHeat - deltaT)
        if self.turretOverHeated and self.turretHeat == 0.0:
            self.turretOverHeated = False

    def getAbsVelocity(self):
        '''
        Return the absolute value of the velocity the player should have
        (assuming the player is living), given the direction that the player is
        facing and the keys (left/right) being pressed.
        '''
        if not self.canMove:
            return 0

        # Consider horizontal movement of player.
        if self._state['left'] and not self._state['right']:
            if self._faceRight:
                return -self.world.physics.playerSlowXVel
            return -self.world.physics.playerXVel

        if self._state['right'] and not self._state['left']:
            if self._faceRight:
                return self.world.physics.playerXVel
            return self.world.physics.playerSlowXVel

        return 0

    def getCurrentVelocity(self):
        '''
        Used to decide how fast the Trosball should go if it's dropped.
        '''
        return (self.getAbsVelocity(), self.yVel)

    def dropThroughFloor(self):
        self._ignore = self.attachedObstacle
        self.detachFromEverything()

    def dropOffWall(self):
        self._unstickyWall = self.attachedObstacle
        self.detachFromEverything()

    def moveAlongGround(self, absVel):
        if absVel == 0:
            return

        deltaT = self.world.tickPeriod
        attachedObstacle = self.attachedObstacle
        for i in xrange(100):
            if deltaT <= 0:
                obstacle = None
                break

            oldPos = self.pos
            deltaX, deltaY = attachedObstacle.walkTrajectory(absVel, deltaT)
            nextSection, corner = attachedObstacle.checkBounds(
                self, deltaX, deltaY)

            # Check for collisions in this path.
            obstacle = self.world.physics.moveUnit(
                self, corner[0] - self.pos[0], corner[1] - self.pos[1],
                ignoreObstacles=attachedObstacle.subshape)
            if obstacle is not None:
                break
            if nextSection is None:
                obstacle = None
                self.setAttachedObstacle(None)
                break
            if nextSection == attachedObstacle:
                obstacle = None
                break

            self.attachedObstacle = attachedObstacle = nextSection
            nextSection.hitByPlayer(self)
            deltaT -= (
                (oldPos[0] - self.pos[0]) ** 2
                + (oldPos[1] - self.pos[1]) ** 2) ** 0.5 / abs(absVel)
        else:
            log.error(
                'Very very bad thing: motion loop did not terminate after '
                '100 iterations')

        if obstacle:
            if obstacle.jumpable:
                if self.isOnGround() and obstacle.grabbable:
                    # Running into a vertical wall while on the ground.
                    pass
                else:
                    self.setAttachedObstacle(obstacle)
            else:
                self.setAttachedObstacle(None)
            obstacle.hitByPlayer(self)

        self._ignore = None

    def setAttachedObstacle(self, obstacle):
        if obstacle and not obstacle.jumpable:
            log.warning('Cannot set attached obstacle to %s', obstacle)
            return
        self.attachedObstacle = obstacle
        self.motionState = self.getAttachedMotionState(obstacle)

    @staticmethod
    def getAttachedMotionState(obstacle):
        if obstacle is None:
            return 'fall'
        if obstacle.grabbable:
            if obstacle.deltaPt[1] < 0:
                return 'rightwall'
            return 'leftwall'
        return 'ground'

    def calculateJumpMotion(self, absVel):
        '''
        Returns (dx, dy, dt) where (dx, dy) is the trajectory due to the upward
        thrust of jumping, and dt is the time for which the upward thrust does
        not apply.
        '''
        deltaT = self.world.tickPeriod
        deltaY = 0
        deltaX = absVel * deltaT

        # If the player is jumping, calculate how much they jump by.
        if self._jumpTime > 0:
            thrustTime = min(deltaT, self._jumpTime)
            self.yVel = -self.world.physics.playerJumpThrust
            deltaY = thrustTime * self.yVel
            self._jumpTime = self._jumpTime - deltaT

            # Automatically switch off the jumping state if the player
            # has reached maximum time.
            if self._jumpTime <= 0:
                self._jumpTime = 0
            return deltaX, deltaY, deltaT - thrustTime
        return deltaX, deltaY, deltaT

    def getFallTrajectory(self, deltaX, deltaY, fallTime):
        # If player is falling, calculate how far they fall.

        # v = u + at
        vFinal = self.yVel + self.world.physics.playerGravity * fallTime
        if vFinal > self.world.physics.playerMaxFallVel:
            # Hit terminal velocity. Fall has two sections.
            deltaY = (
                deltaY + (
                    self.world.physics.playerMaxFallVel ** 2 - self.yVel ** 2
                ) / (2 * self.world.physics.playerGravity)
                + self.world.physics.playerMaxFallVel * (fallTime - (
                    self.world.physics.playerMaxFallVel - self.yVel
                ) / self.world.physics.playerGravity))

            self.yVel = self.world.physics.playerMaxFallVel
        else:
            # Simple case: s=ut+0.5at**2
            deltaY = (
                deltaY + self.yVel * fallTime + 0.5 *
                self.world.physics.playerGravity * fallTime ** 2)
            self.yVel = vFinal

        return deltaX, deltaY

    def fallThroughAir(self, absVel):
        deltaX, deltaY, fallTime = self.calculateJumpMotion(absVel)
        deltaX, deltaY = self.getFallTrajectory(deltaX, deltaY, fallTime)

        obstacle = self.world.physics.moveUnit(self, deltaX, deltaY)
        if obstacle:
            if obstacle == self._unstickyWall:
                targetPt = obstacle.unstickyWallFinalPosition(
                    self.pos, deltaX, deltaY)
            else:
                targetPt = obstacle.finalPosition(self, deltaX, deltaY)
            if targetPt is not None:
                deltaX = targetPt[0] - self.pos[0]
                deltaY = targetPt[1] - self.pos[1]
                obstacle = self.world.physics.moveUnit(self, deltaX, deltaY)

        if obstacle and obstacle.jumpable:
            self.setAttachedObstacle(obstacle)
        else:
            self.setAttachedObstacle(None)
        if obstacle:
            obstacle.hitByPlayer(self)

        self._ignore = None

    def updateLivingPlayer(self):
        self.processJumpState()

        absVel = self.getAbsVelocity()
        wall = self.isAttachedToWall()

        # Allow falling through fall-through-able obstacles
        if self.isOnPlatform() and self._state['down'] and self.canMove:
            self.dropThroughFloor()
        if self.isOnGround():
            self.moveAlongGround(absVel)
        elif wall:
            if (
                    self._state['down']
                    or (self._state['right'] and wall == 'left')
                    or (self._state['left'] and wall == 'right')
                    or not self.canMove
                    ):
                self.dropOffWall()
        else:
            self.fallThroughAir(absVel)

    def advance(self):
        '''Called by this player's universe when this player should update
        its position. deltaT is the time that's passed since its state was
        current, measured in seconds.'''

        if self.resyncing:
            return

        self.checkUpgrades()
        self.reloadTime = max(0.0, self.reloadTime - self.world.tickPeriod)

        if self.knowsItsDead:
            self.updateGhost()
        elif self.turret:
            self.updateTurret()
        else:
            self.updateLivingPlayer()

        if self.attachedObstacle:
            self.pos = self.attachedObstacle.discretise(Player, self.pos)
        else:
            self.pos = (floor(self.pos[0] + 0.5), floor(self.pos[1] + 0.5))

    def isOnside(self, trosballPosition):
        onLeftOfBall = self.pos[0] < trosballPosition[0]
        onBlueTeam = self.team == self.world.teams[0]
        return onLeftOfBall == onBlueTeam

    def hitShield(self, shooter, deathType):
        '''
        Hits the shield for one point of damage, and returns True if the shield
        absorbed the damage, False if there was no shield.
        '''
        if self.hasProtectiveUpgrade():
            self.upgrade.protections -= 1
            if self.upgrade.protections <= 0:
                self.deleteUpgrade()
                self.onShieldDestroyed(shooter, deathType)
                if self in self.world.players and shooter:
                    shooter.onDestroyedShield(self, deathType)
            return True
        return False

    def zombieHit(self, shooter, shot, deathType):
        '''
        Called when the player has been hit, but the player's client may not
        realise that the player is dead yet.
        '''
        self.zombieHits += 1
        self.onZombieHit(shooter, shot, deathType)

    def properHit(self, shooter, deathType):
        '''
        Called when the player has been hit AND the client is guaranteed to be
        the first one to notice it (because it relates to where the player
        thinks it is rather than where the server thinks the player is).
        '''
        if not self.hitShield(shooter, deathType):
            self.health -= 1
            self.checkDeath(shooter, deathType)

    def noticeZombieHit(self, shooter, deathType):
        '''
        Called when the player notices that it's been hit.
        '''
        assert self.zombieHits >= 0
        self.zombieHits -= 1
        self.properHit(shooter, deathType)

    def killOutright(self, deathType, killer=None, resync=True):
        self.health = 0
        self.checkDeath(killer, deathType)

        # An outright kill cannot be detected by the client until it happens,
        # so the client will have mis-predicted where the player is going and
        # will need to resync.
        if resync:
            self.sendResync(reason='')

    def checkDeath(self, killer, deathType):
        if self.dead:
            if self.hasTrosball():
                self.world.trosballLost(self)
            if self.hasElephant():
                self.world.elephantKill(killer)

        if self.knowsItsDead:
            self.health = 0
            self.zombieHits = 0
            self.respawnGauge = self.world.physics.playerRespawnTotal
            self._jumpTime = 0
            self.pendingUpgrade = None
            self.deleteUpgrade()
            self._setStarsForDeath()
            self.setAttachedObstacle(None)
            if self in self.world.players:
                if killer:
                    killer.onKilled(self, deathType)
                    self.world.onPlayerKill(killer, self, deathType)
                self.world.playerHasNoticedDeath(self, killer)
            self.onDied(killer, deathType)

    def _setStarsForDeath(self):
        self.starsAtLastDeath = self.stars
        self.stars = self.world.PLAYER_RESET_STARS
        self.onStarsChanged()

    def respawn(self, zone=None):
        if self.resyncing:
            return
        self.setAttachedObstacle(None)
        self.health = self.world.physics.playerRespawnHealth
        self.zombieHits = 0
        self.invulnerableUntil = (
            self.world.timer.getElapsedTime() + RESPAWN_CAMP_TIME)
        self.respawnGauge = 0
        self.teleportToZoneCentre(zone)
        self.world.onPlayerRespawn(self)
        self.onRespawned()

    def teleportToZoneCentre(self, zone=None):
        if zone is None:
            zone = self.getZone()
        self.setPos(zone.defn.pos, 'f')

    def deleteUpgrade(self, abandoned=False):
        '''Deletes the current upgrade object from this player'''
        if self.resyncing:
            return
        upgrade = self.upgrade
        if upgrade:
            upgrade.delete()
            if abandoned:
                self.onAbandonUpgrade(upgrade)
            self.onUpgradeGone(upgrade)

    def incrementStars(self):
        if self.stars < MAX_STARS:
            self.stars += 1
            self.onStarsChanged()

    def getShotType(self):
        '''
        Returns one of the following:
            None - if the player cannot currently shoot
            'N' - if the player can shoot normal shots
            'R' - if the player can shoot ricochet shots
            'T' - if the player can shoot turret shots
        '''
        if self.dead or self.phaseshift or not self.canMove:
            return None

        # While on a vertical wall, one canst not fire
        if self.reloadTime > 0 or self.isAttachedToWall():
            return None

        if self.hasRicochet:
            return Shot.RICOCHET
        if self.turret:
            if self.turretOverHeated:
                return None
            return Shot.TURRET
        return Shot.NORMAL

    def setUser(self, user):
        if not self.bot:
            self.user = user

    def isElephantOwner(self):
        return self.user is not None and self.user.isElephantOwner()

    def hasElephant(self):
        playerWithElephant = self.world.playerWithElephant
        return playerWithElephant and playerWithElephant.id == self.id

    def canShoot(self):
        return self.getShotType() is not None

    def sendResync(
            self, reason='Your computer was out of sync with the server!'):
        args = self.getPlayerUpdateArgs(resync=True)
        globalMsg, resyncMsg = PlayerUpdateMsg(*args), ResyncPlayerMsg(*args)
        if self.resyncing and self.checkResyncAcknowledgement(resyncMsg):
            # No need to send the second resync, the player is still in the
            # same state.
            return
        if not self.world.isServer:
            return
        self.world.sendServerCommand(globalMsg)
        if self.agent:
            self.agent.messageToAgent(resyncMsg)
            if reason:
                self.agent.messageToAgent(
                    ChatFromServerMsg(error=True, text=reason))
        self.resyncBegun()

    def resyncBegun(self):
        self.resyncing = True
        self.resyncExpiry = self.world.lastTickId + int(
            MAX_RESYNC_TIME / self.world.tickPeriod)

    def getPlayerUpdateArgs(self, resync=None):
        attached = self.motionState[0]

        if resync is None:
            resync = self.resyncing

        health = max(self.health - self.zombieHits, 0)

        return (
            self.id, self.pos[0], self.pos[1], self.yVel, self.angleFacing,
            self.ghostThrust, self._jumpTime, self.reloadTime,
            self.respawnGauge, attached, self.stars, health, resync,
            self._state['left'], self._state['right'], self._state['jump'],
            self._state['down'])

    def applyPlayerUpdate(self, msg):
        self._state['left'] = msg.leftKey
        self._state['right'] = msg.rightKey
        self._state['jump'] = msg.jumpKey
        self._state['down'] = msg.downKey

        self.yVel = msg.yVel
        self.lookAt(msg.angle, msg.ghostThrust)
        self.setPos((msg.xPos, msg.yPos), msg.attached)
        self._jumpTime = msg.jumpTime
        self.reloadTime = msg.gunReload
        self.respawnGauge = msg.respawn
        oldStars = self.stars
        self.stars = msg.stars
        self.health = msg.health
        self.zombieHits = 0
        if msg.resync:
            self.resyncBegun()
        else:
            self.resyncing = False
        if oldStars != self.stars:
            self.onStarsChanged()

    def buildResyncAcknowledgement(self):
        return ResyncAcknowledgedMsg(
            self.world.lastTickId, self.pos[0], self.pos[1],
            self.yVel, self.angleFacing, self.ghostThrust)

    def checkResyncAcknowledgement(self, msg):
        '''
        Checks whether the player position etc. matches the position encoded in
        the ResyncPlayerMsg or ResyncAcknowledgedMsg.
        '''
        return (
            isNear(self.pos[0], msg.xPos)
            and isNear(self.pos[1], msg.yPos)
            and isNear(self.yVel, msg.yVel)
            and isNear(self.angleFacing, msg.angle)
            and isNear(self.ghostThrust, msg.ghostThrust))

    def weaponDischarged(self):
        '''
        Updates the player's reload time because the player has just fired a
        shot.
        '''
        world = self.world
        zone = self.getZone()
        if self.turret:
            reloadTime = world.physics.playerTurretReloadTime
            self.turretHeat += world.physics.playerShotHeat
            if self.turretHeat > world.physics.playerTurretHeatCapacity:
                self.turretOverHeated = True
        elif self.machineGunner:
            self.mgBulletsRemaining -= 1
            if self.mgBulletsRemaining > 0:
                reloadTime = world.physics.playerMachineGunFireRate
            elif self.mgBulletsRemaining == 0:
                reloadTime = world.physics.playerMachineGunReloadTime
            else:
                self.mgBulletsRemaining = 15
                reloadTime = 0
        elif self.shoxwave:
            reloadTime = world.physics.playerShoxwaveReloadTime
        elif self.team is None:
            reloadTime = world.physics.playerNeutralReloadTime
        elif world.state.isTrosball():
            if abs(self.pos[0] - world.getTrosballPosition()[0]) < 1e-5:
                reloadTime = world.physics.playerNeutralReloadTime
            # If self is on blue, and on the left of the trosball; or
            # completely vice versa
            elif self.isOnside(world.getTrosballPosition()):
                reloadTime = world.physics.playerOwnDarkReloadTime
            else:
                reloadTime = world.physics.playerEnemyDarkReloadTime
        elif zone and zone.owner == self.team and zone.dark:
            reloadTime = world.physics.playerOwnDarkReloadTime
        elif zone and not zone.dark:
            reloadTime = world.physics.playerNeutralReloadTime
        else:
            reloadTime = world.physics.playerEnemyDarkReloadTime
        self.reloadTime = self.reloadFrom = reloadTime

    def createShot(self, shotId=None, shotClass=Shot):
        '''
        Factory function for building a Shot object.
        '''
        # Shots take some fraction of the player's current velocity, but we
        # still want the shots to always go directly towards where the user
        # clicked, so we take the component of player velocity in the direction
        # of the shot.
        f = self.world.physics.fractionOfPlayerVelocityImpartedToShots
        xVel = (self.pos[0] - self.oldPos[0]) / self.world.tickPeriod
        yVel = (self.pos[1] - self.oldPos[1]) / self.world.tickPeriod
        shotVel = self.world.physics.shotSpeed + f * (
            xVel * sin(self.angleFacing) - yVel * cos(self.angleFacing))

        velocity = (
            shotVel * sin(self.angleFacing),
            -shotVel * cos(self.angleFacing),
        )

        kind = self.getShotType()
        lifetime = self.world.physics.shotLifetime

        team = self.team
        shot = shotClass(
            self.world, shotId, team, self, self.pos, velocity, kind, lifetime)
        return shot
