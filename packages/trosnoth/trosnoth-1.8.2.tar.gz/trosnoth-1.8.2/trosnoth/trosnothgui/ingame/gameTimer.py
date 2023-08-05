import logging
import pygame

from trosnoth.gui.framework.elements import TextElement
from trosnoth.gui.framework import clock, timer
from trosnoth.gui.common import (
    Area, FullScreenAttachedPoint, Location, ScaledSize,
)
import trosnoth.gui.framework.framework as framework
from trosnoth.model import gameStates
from trosnoth.utils.twist import WeakCallLater

log = logging.getLogger(__name__)


class GameTimer(framework.CompoundElement):
    def __init__(self, app, game):
        super(GameTimer, self).__init__(app)
        self.world = game.world
        self.app = app

        # Change these constants to say where the box goes
        self.area = Area(
            FullScreenAttachedPoint(ScaledSize(0, -3), 'midtop'),
            ScaledSize(110, 35),
            'midtop')

        self.lineWidth = max(int(3*self.app.screenManager.scaleFactor), 1)
        # Anything more than width 2 looks way too thick
        if self.lineWidth > 2:
            self.lineWidth = 2
        self.notStarted = TextElement(
            self.app, "--:--", self.app.screenManager.fonts.timerFont,
            Location(
                FullScreenAttachedPoint(ScaledSize(0, -9), 'midtop'),
                'midtop'),
            app.theme.colours.timerFontColour)
        self.elements = [self.notStarted]
        self.running = False

        self.gameTimer = None
        self.gameClock = None
        self.timerAdjustLoop = None
        self.mode = 'none'

        # Seconds for two flashes
        self.flashCycle = 0.5
        # Value the countdown has to get to before it starts to flash
        self.flashValue = 30

        self.loop()

    def loop(self):
        self.timerAdjustLoop = WeakCallLater(10, self, 'loop')
        self.syncTimer()

    def checkState(self):
        if self.mode != self.getWorldMode():
            self.mode = self.getWorldMode()

            if self.running and self.mode == 'stopped':
                self.stopTimer()
            elif (not self.running) and self.mode != 'stopped':
                self.startTimer()
            else:
                self.resetTimer()

    def syncTimer(self):
        if self.gameTimer is None:
            return

        if self.mode == 'starting':
            self.gameTimer.counted = self.gameStartCountdownClock()
            self.gameTimer.countTo = self.world.timer.getStartCountdownMax()
        else:
            self.gameTimer.counted = self.world.timer.getElapsedTime()
            if self.world.timer.hasTimeLimit():
                self.gameTimer.countTo = self.world.timer.getMatchDuration()

    def _flash(self, flashState):
        if flashState == 0:
            self.gameClock.setColours(self.app.theme.colours.timerFlashColour)
        else:
            self.gameClock.setColours(self.app.theme.colours.timerFontColour)

    def kill(self):
        if (self.world.state == gameStates.InProgress and
                self.timerAdjustLoop is not None):
            self.timerAdjustLoop.cancel()
        self.gameTimer = None

    def startTimer(self):
        self.running = True
        self.gameClock = clock.Clock(
            self.app,
            None,   # We'll set the timer soon...
            Location(FullScreenAttachedPoint(
                ScaledSize(0, 0), 'midtop'), 'midtop'),
            self.app.screenManager.fonts.timerFont,
            self.app.theme.colours.timerFontColour)

        self.resetTimer()
        self.elements = [self.gameClock]

    def getWorldMode(self):
        if self.world.state.isStartingCountdown():
            return 'starting'
        if self.world.state.getGameTimeMode() != 'running':
            return 'stopped'
        if self.world.timer.hasTimeLimit():
            return 'countdown'
        return 'countup'

    def gameStartCountdownClock(self):
        t = self.world.timer
        # We subtract 0.999 so that the timer is rounding up the seconds rather
        # than rounding them down. This is so that the instant it hits zero,
        # the game starts.
        return t.getStartCountdownMax() - t.getStartCountdown() - 0.999

    def resetTimer(self):
        self.mode = self.getWorldMode()
        if self.mode == 'starting':
            self.gameTimer = timer.CountdownTimer(
                highest='minutes', clock=self.gameStartCountdownClock)
        elif self.mode == 'countdown':
            self.gameTimer = timer.CountdownTimer(
                highest='minutes', clock=self.world.timer.getElapsedTime)
        else:
            self.gameTimer = timer.Timer(
                highest='minutes', clock=self.world.timer.getElapsedTime)
        if self.gameClock is not None:
            self.gameClock.setTimer(self.gameTimer)
            self._flash(1)
        self.syncTimer()
        self.gameTimer.start()

    def stopTimer(self):
        self.running = False
        if self.timerAdjustLoop is not None:
            self.timerAdjustLoop.cancel()
            self.timerAdjustLoop = None
            self.gameTimer.pause()
            if self.gameClock:
                self.gameClock.setColours(
                    self.app.theme.colours.timerFontColour)
            self.gameTimer = None
        self.elements = [self.notStarted]

    def _getRect(self):
        return self.area.getRect(self.app)

    def tick(self, deltaT):
        super(GameTimer, self).tick(deltaT)
        self.checkState()
        if (
                self.running and self.mode == 'countdown'
                and self.gameTimer is not None
                and self.gameTimer.getCurTime() <= self.flashValue):
            self._flash(
                int((self.gameTimer.getCurTime() / self.flashCycle) % 2))

    def draw(self, surface):
        timerBox = self._getRect()
        # Box background
        surface.fill(self.app.theme.colours.timerBackground, timerBox)

        # Box border
        pygame.draw.rect(
            surface, self.app.theme.colours.black, timerBox, self.lineWidth)

        super(GameTimer, self).draw(surface)
