import RPi.GPIO as gpio

from pyparts.platforms.pwm import base_pwm


class RaspberryPiPWMOutput(base_pwm.BasePWM):
  """Raspberry Pi implementation of a PWM peripheral.
  
  Attributes:
    _pwm_pin: DigitalOutput. The pin being used for PWM.
  """

  def __init__(self, output_pin, frequency_hz=2000):
    """Creates a PWM output on a DigitalOutput pin.
    
    Args:
      output_pin: DigitalOutput. A DigitalOutput pin to use for PWM output.
      frequency_hz: Float. PWM frequency to use. (default=2000)
    """
    super(RaspberryPiPWMOutput, self).__init__(output_pin)
    self._pwm_pin = gpio.PWM(self._output_pin.pin_number, frequency_hz)

  def _enable(self):
    """Enables the PWM output."""
    self._pwm_pin.start(0)

  def _disable(self):
    """Disables the PWM output."""
    self._pwm_pin.stop()

  def _set_duty_cycle(self, duty_cycle):
    """Sets the duty cycle for the PWM output.

    Args:
      duty_cycle: Float from 0.0 to 100.0. Duty cycle to set the PWM output to.
    """
    self._pwm_pin.ChangeDutyCycle(duty_cycle)

  def _set_frequency_hz(self, frequency_hz):
    """Sets the frequency for the PWM output.

    Args:
      frequency_hz: Float. The frequency to set the PWM output to in Hertz.
    """
    self._pwm_pin.ChangeFrequency(frequency_hz)
