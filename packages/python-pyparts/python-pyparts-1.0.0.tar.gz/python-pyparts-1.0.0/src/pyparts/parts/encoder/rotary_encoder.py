import math
import time
import threading

from pyparts.parts import base_part


class RotaryEncoder(base_part.BasePart):

  def __init__(self, a_pin, b_pin):
    self._a = a_pin
    self._b = b_pin

    self._last_state = self.get_state()
    self._last_delta = 0

  def get_state(self):
    a = 1 if self._a.is_high else 0
    b = 1 if self._b.is_high else 0
    return (a ^ b) | b << 1

  def get_delta(self):
    delta = 0
    state = self.get_state()
    if state != self._last_state:
      delta = (state - self._last_state) % 4
      if delta == 3:
        delta = -1
      elif delta == 2:
        # Assume two steps in the same direction as the previous step.
        delta = int(math.copysign(delta, self._last_delta))
      self._last_state = state
      self._last_delta = delta
    return delta

  class Worker(threading.Thread):

    def __init__(self, a_pin, b_pin):
      super(RotaryEncoder.Worker, self).__init__()
      self._lock = threading.Lock()
      self._encoder = RotaryEncoder(a_pin, b_pin)
      self._delta = 0
      self._stop = False

    def run(self):
      while not self._stop:
        delta = self._encoder.get_delta()
        with self._lock:
          self._delta += delta
        time.sleep(0.001)

    def stop(self):
      self._stop = True

    def get_delta(self):
      with self._lock:
        delta = self._delta
        self._delta = 0
      return delta
