 
import time
import math

class timer:
    _running = False
    _timeLast = 0

    def start(self):
        self._timeLast = self._now()
        self._running = True

    def stop(self):
        self._running = False

    def reset(self):
        self._timeLast = self._now()

    def isRunning(self):
        return self._running

    def readSec(self):
        return math.floor(self.readMs() / 1000)

    def readMs(self):
        if (self._running is False):
            return 0

        return self._now() - self._timeLast

    def _now(self):
        return math.floor(time.time() * 1000)
