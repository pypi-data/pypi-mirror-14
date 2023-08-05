from math import pi
import random
from trosnoth.ai import AI

from trosnoth.model.upgrades import Grenade
from twisted.internet import reactor, task


class JohnAI(AI):
    '''
    In version 1.1.3 the computer(AI) players have the following functions:
    1. The robot runs "intelligently" around the map until it gets confused
        with a block.
    2. The robot's shooting is randomly off to make it more human like.
    3. The  robot gets confused less
    4. The robot talks less
    5. The robot gets confused by Minimap Disruption
    6. The robot don't shoot players that are invisible.
    7. Uses Grenades when there are 3 players in its current zone
    This file was edited by John "AIMaker" Board at home. 28/12/10 3:57 PM
    '''

    nick = 'JohnBot'
    playable = True

    def start(self):
        self._pauseTimer = None
        self._loop = task.LoopingCall(self.tick)
        self._loop.start(0.5)

    def disable(self):
        self._loop.stop()
        if self._pauseTimer is not None:
            self._pauseTimer.cancel()

    def tick(self):
        self.beforeX = self.player.pos[0]
        if self.player.dead:
            if self.player.inRespawnableZone():
                self.doAimAt(0, thrust=0)
                if self.player.respawnGauge == 0:
                    self.doRespawn()
            else:
                self.aimAtFriendlyZone()
        else:
            if self._pauseTimer is None:
                self.startPlayerMoving()
            if self.player.canShoot():
                self.fireAtNearestEnemy()
            self.useUpgrade()

    def checkEnemyUpgrade(self):
        enemies = [p for p in self.world.players if not
                   (p.dead or self.player.isFriendsWith(p))]
        upgrade = [str(p.upgrade) for p in enemies if p.upgrade is not None]
        return upgrade

    def useUpgrade(self):
        if len(self.getEnemyPlayersInZone()) > 3:
            self.doBuyUpgrade(Grenade)

    def aimAtFriendlyZone(self):
        zones = [z for z in self.world.zones if z.owner == self.player.team]
        if len(zones) == 0:
            return

        def getZoneDistance(zone):
            x1, y1 = self.player.pos
            x2, y2 = zone.defn.pos
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        bestZone = min(zones, key=getZoneDistance)
        self.doAimAtPoint(bestZone.defn.pos)

    def fireAtNearestEnemy(self):
        enemies = [
            p for p in self.world.players
            if not (p.dead or p.invisible or self.player.isFriendsWith(p))]
        if len(enemies) == 0:
            return

        def getPlayerDistance(p):
            x1, y1 = self.player.pos
            x2, y2 = p.pos
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        nearestEnemy = min(enemies, key=getPlayerDistance)
        # If you get closer than these many pixels you will get shot at, orig
        # value = 512, it is determined by the difficulty rating
        if getPlayerDistance(nearestEnemy) < 300:
            # Do not shoot at ninjas
            if not nearestEnemy.invisible:
                # Add "human" error to nearest enemy pos
                pos = (
                    nearestEnemy.pos[0] + (random.random() * 100),
                    nearestEnemy.pos[1] + (random.random() * 100))
                self.doAimAtPoint(pos)
                self.doShoot()

    def totalOfEnemies(self):
        enemies = [
            p for p in self.world.players
            if not (p.dead or self.player.isFriendsWith(p))]
        return len(enemies)

    def getEnemyPlayersInZone(self):
        return [
            p for p in self.player.getZone().players
            if not (p.dead or self.player.isFriendsWith(p))]

    def getEnemyPlayerCount(self):
        return len(self.getEnemyPlayersInZone())

    def died(self, killer, deathType):
        self._pauseTimer = None
        self.doStop()
        self.aimAtFriendlyZone()

    def respawned(self):
        self.startPlayerMoving()

    def startPlayerMoving(self):
        self.pauseAndReconsider()

    def posOfOrb(self):
        return self.player.getZone().defn.pos

    def pauseAndReconsider(self):
        self.beforeX = self.player.pos[0]
        if self.player.dead:
            self._pauseTimer = None
            return

        # Pause again in between 0.5 and 2.5 seconds time.
        t = random.random() * 0.2 + 0.2
        self._pauseTimer = reactor.callLater(t, self.pauseAndReconsider)

        # Decide on a direction.
        def getPlayerDistance(p):
            x1, y1 = self.player.pos
            x2, y2 = p.pos
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        enemies = [
            p for p in self.world.players
            if not (p.dead or self.player.isFriendsWith(p))]
        if len(enemies) > 0:
            nearestEnemy = min(enemies, key=getPlayerDistance)
        if "Minimap Disruption" in self.checkEnemyUpgrade():
                self.randomMove()
        if len(enemies) > 0:
            if self.player.getZone().owner == self.player.team:
                x = nearestEnemy.pos[0]
                y = nearestEnemy.pos[1]
                self.moveToward(x, y)
        elif not self.player.getZone():
            pass
        elif not self.player.getZone().owner == self.player.team:
            if self.getEnemyPlayerCount() == 0:
                x = self.posOfOrb()[0]
                y = self.posOfOrb()[1]
                self.moveToward(x, y)

    def randomMove(self):
        d = random.choice(['drop', 'jump', 'left', 'right'])
        if d == 'drop':
            self.doDrop()
        if d == 'jump':
            self.doJump()
        if d == 'left':
            self.doMoveLeft()
        if d == 'right':
            self.doMoveRight()

    def moveToward(self, x, y):
        if x > self.player.pos[0] and self.player.isAttachedToWall():
            self.doAimAt(pi / 2.)
            self.doMoveRight()
            self.doJump()
        if x < self.player.pos[0] and self.player.isAttachedToWall():
            self.doAimAt(-pi / 2.)
            self.doMoveLeft()
            self.doJump()
        if x > self.player.pos[0] and self.player.isOnGround():
            self.doAimAt(pi / 2.)
            self.doMoveRight()
            self.doJump()
        if x < self.player.pos[0] and self.player.isOnGround():
            self.doAimAt(-pi / 2.)
            self.doMoveLeft()
            self.doJump()
        if y > self.player.pos[1] and self.player.isOnPlatform():
            self.doDrop()
        if y < self.player.pos[1]:
            self.doJump()
        if x == self.player.pos[0] and y < self.player.pos[1]:
            self.doJump()
        if x == self.player.pos[0] and y > self.player.pos[1]:
            self.doDrop()

AIClass = JohnAI
