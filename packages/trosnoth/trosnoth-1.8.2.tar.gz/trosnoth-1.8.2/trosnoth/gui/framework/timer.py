import datetime
import logging

from trosnoth.gui.framework import framework
from trosnoth.utils.event import Event

log = logging.getLogger(__name__)


class ITimer(framework.Element):
    def __init__(self, clock=None):
        self.running = False
        self.clock = clock
        if clock:
            self.lastClockTime = clock()
        else:
            self.lastClockTime = None

    def getDelta(self, delta):
        if self.clock:
            now = self.clock()
            delta = now - self.lastClockTime
            self.lastClockTime = now
        return delta

    def start(self):
        self.running = True
        return self

    def pause(self):
        self.running = False
        return self

    def tick(self, deltaT):
        raise NotImplementedError('%s.tick' % (self.__class__.__name__,))

    def getTimeString(self):
        raise NotImplementedError(
            '%s.getTimeString' % (self.__class__.__name__,))


class CountdownTimer(ITimer):
    '''
    @param amount    Amount of time to count down
    '''

    def __init__(self, countTo=0, highest="days", *args, **kwargs):
        super(CountdownTimer, self).__init__(*args, **kwargs)
        self.countTo = countTo
        self.counted = 0
        self.onCountedDown = Event()
        self.highest = highest

    def tick(self, deltaT):
        deltaT = self.getDelta(deltaT)
        if self.running:
            self.counted += deltaT

            if self.counted > self.countTo:
                self.counted = self.countTo
                self.onCountedDown.execute()

    def getCurTime(self):
        return max(0, self.countTo - self.counted)

    def getTimeString(self):
        total = int(self.getCurTime())
        deltaResult = datetime.timedelta(seconds=total)
        seconds = deltaResult.days * 24 * 60 * 60 + deltaResult.seconds
        if self.highest == "seconds":
            return str(seconds)
        elif self.highest == "minutes":
            minutes, seconds = divmod(seconds, 60)
            return "%02d:%02d" % (minutes, seconds)
        elif self.highest == "hours":
            hours, minutes = divmod(minutes, 60)
            return "%d:%02d:%02d" % (hours, minutes, seconds)
        else:
            return str(deltaResult)


class Timer(ITimer):
    '''@param tick  Frequency with which onTick events are triggered.'''
    def __init__(
            self, tickDuration=1, startAt=None, highest="days",
            *args, **kwargs):
        super(Timer, self).__init__(*args, **kwargs)
        if startAt is None:
            self.counted = 0
        else:
            self.counted = startAt
        self.tickDuration = tickDuration
        self.highest = highest

        self.onTick = Event()

    def tick(self, deltaT):
        deltaT = self.getDelta(deltaT)
        if self.running:
            numTicked = self.counted / self.tickDuration
            self.counted += deltaT
            if (self.counted / self.tickDuration) > numTicked:
                self.onTick.execute()

    def getTimeString(self):
        deltaResult = datetime.timedelta(seconds=int(max(0, self.counted)))
        seconds = deltaResult.days * 24 * 60 * 60 + deltaResult.seconds
        if self.highest == "seconds":
            return str(seconds)
        elif self.highest == "minutes":
            minutes, seconds = divmod(seconds, 60)
            return "%02d:%02d" % (minutes, seconds)
        elif self.highest == "hours":
            hours, minutes = divmod(minutes, 60)
            return "%d:%02d:%02d" % (hours, minutes, seconds)
        else:
            return str(deltaResult)
