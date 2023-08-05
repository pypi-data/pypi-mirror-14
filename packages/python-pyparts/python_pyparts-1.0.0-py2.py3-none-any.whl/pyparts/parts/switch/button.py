from pyparts.parts import base_part


class Button(base_part.BasePart):
  
  def __init__(self, pin):
    self._pin = pin
    self._enabled = False

  def set_on_down(self, callback, debounce_time_ms):
    if self._pin.pull_up_down == self._pin.PUD_UP:
      type = self._pin.INTERRUPT_FALLING
    else:
      type = self._pin.INTERRUPT_RISING
    self._pin.add_interrupt(type, callback, debounce_time_ms)

  def set_on_up(self, callback, debounce_time_ms):
    if self._pin.pull_up_down == self._pin.PUD_UP:
      type = self._pin.INTERRUPT_RISING
    else:
      type = self._pin.INTERRUPT_FALLING
    self._pin.add_interrupt(type, callback, debounce_time_ms)

  def set_on_both(self, callback, debounce_time_ms):
    self._pin.add_interrupt(self._pin.INTERRUPT_BOTH, callback,
                            debounce_time_ms)

  def set_on_hold(self, callback, min_hold_time):
    raise NotImplementedError

  def set_on_press(self, callback, max_down_time):
    raise NotImplementedError

  def set_on_double_press(self, callback, max_down_time, max_up_time):
    raise NotImplementedError

  def remove_callbacks(self):
    self._pin.remove_interrupt()
