from trosnoth.ais.alpha import AlphaAI

from twisted.internet import task


class TestingAI(AlphaAI):
    nick = 'TestBot'
    playable = True

    # Use these toggles to change the behaviour of the bots.
    canMove = True
    canShoot = True
    canJump = True
    upgradeType = None

    def start(self):
        super(TestingAI, self).start()
        self._loop = task.LoopingCall(self.tick)
        self._loop.start(0.5)

    def tick(self):
        if (not self.player.dead and self.player.upgrade is None
               and self.upgradeType is not None):
            self.doBuyUpgrade(self.upgradeType)

    def shoot(self):
        if self.canShoot:
            super(TestingAI, self).shoot()

    def changeXDir(self):
        if self.canMove:
            super(TestingAI, self).changeXDir()

    def jumpAgain(self):
        if self.canJump:
            super(TestingAI, self).jumpAgain()

AIClass = TestingAI
