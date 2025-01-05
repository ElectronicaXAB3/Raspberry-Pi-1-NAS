from threading import Timer

class ElapsedTimer:
    def __init__(self, interval: float):
        self._elapsed = False
        self._interval = interval
        self._timer = None
        self._start_timer()

    def elapsed(self):
        return self._elapsed

    def reset(self):
        self._elapsed = False
        self._start_timer()

    def _start_timer(self):
        self._timer = Timer(self._interval, self._set_elapsed)
        self._timer.start()

    def _set_elapsed(self):
        self._elapsed = True
