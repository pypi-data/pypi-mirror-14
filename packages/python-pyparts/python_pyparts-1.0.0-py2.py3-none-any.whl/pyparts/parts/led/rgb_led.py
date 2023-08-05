import time

from pyparts.parts import base_part


class RGBLed(base_part.BasePart):

  def __init__(self, red_pwm, blue_pwm, green_pwm):
    self._red_pwm = red_pwm
    self._green_pwm = green_pwm
    self._blue_pwm = blue_pwm

  def enable(self):
    self._red_pwm.enable()
    self._green_pwm.enable()
    self._blue_pwm.enable()

  def disable(self):
    self._red_pwm.disable()
    self._green_pwm.disable()
    self._blue_pwm.disable()

  @property
  def is_enabled(self):
    return self._red_pwm.is_enabled

  @property
  def pwm_frequency_hz(self):
    return self._red_pwm.frequency_hz

  def set_pwm_frequency_hz(self, frequency_hz):
    self._red_pwm.set_frequency_hz(frequency_hz)
    self._green_pwm.set_frequency_hz(frequency_hz)
    self._blue_pwm.set_frequency_hz(frequency_hz)

  @property
  def rgb(self):
    return self.red, self.green, self.blue

  def set_rgb(self, red_duty_cycle, green_duty_cycle, blue_duty_cycle):
    self.set_red(red_duty_cycle)
    self.set_green(green_duty_cycle)
    self.set_blue(blue_duty_cycle)

  @property
  def red(self):
    return self._red_pwm.duty_cycle

  def set_red(self, duty_cycle):
    self._red_pwm.set_duty_cycle(duty_cycle)

  @property
  def green(self):
    return self._green_pwm.duty_cycle

  def set_green(self, duty_cycle):
    self._green_pwm.set_duty_cycle(duty_cycle)

  @property
  def blue(self):
    return self._blue_pwm.duty_cycle

  def set_blue(self, duty_cycle):
    self._blue_pwm.set_duty_cycle(duty_cycle)

  def fade(self, red, green, blue, delay_ms=500, step=5):
    for i in range(0, delay_ms, step):
      f = float(i) / delay_ms
      self.set_red(self.red + (red - self.red) * f)
      self.set_green(self.green + (green - self.green) * f)
      self.set_blue(self.blue + (blue - self.blue) * f)
      time.sleep(delay_ms / 1000)
