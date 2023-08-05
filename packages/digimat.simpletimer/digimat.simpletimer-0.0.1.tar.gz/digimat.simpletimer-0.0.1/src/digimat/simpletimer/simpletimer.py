import time
from threading import Event


class SimpleTimer(object):
    def __init__(self, delay=0):
        self._delay=float(delay)
        self._delay0=delay
        self._stampStart=0
        self._stampStop=0
        self._timeout=0
        self._eventStart=Event()
        self._eventTimeout=Event()
        self._eventPendingTimeout=Event()
        self.start()

    def start(self, delay=None):
        self.stop()
        if delay is not None:
            self._delay=float(delay)

        self._stampStart=time.time()
        self._timeout=self._stampStart+self._delay
        self._eventStart.set()

    def startWithImmediateTimeout(self):
        self.start(0)

    def restart(self):
        self.start()

    def isStarted(self):
        return self._eventStart.isSet()

    def stop(self):
        self._eventStart.clear()
        self._eventTimeout.clear()
        self._eventPendingTimeout.clear()
        self._stampStop=time.time()

    def getElapsedTime(self):
        if self.isStarted():
            return time.time()-self._stampStart
        return self._stampStop-self._stampStart

    def isElapsedTime(self, delay):
        if self.getElapsedTime()>=delay:
            return True

    def getRemainingTimeToTimeout(self):
        if self.isStarted() and self._delay>0:
            if not self.isTimeout():
                return self._timeout-time.time()
        return 0

    def isTimeout(self):
        if self.isStarted():
            if self._eventTimeout.isSet():
                return True
            if time.time()>=self._timeout:
                self._eventTimeout.set()
                self._eventPendingTimeout.set()
                return True

    def isPendingTimeout(self):
        if self.isTimeout() and self._eventPendingTimeout.isSet():
            self._eventPendingTimeout.clear()
            return True

    def resetToFactorySetting(self):
        self.stop()
        self._delay=self._delay0


if __name__ == "__main__":
    pass
