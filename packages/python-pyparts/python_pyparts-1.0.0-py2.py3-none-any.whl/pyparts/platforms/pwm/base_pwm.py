import abc


class BasePWM(object):
  """A class for creating PWM type peripherals.

  BasePWM implements methods to interact with a PWM interface. Platforms are
  expected to subclass BasePWM and provide platform specific implementations of
  _enable, _disable, _set_duty_cycle, and _set_frequency_hz.

  Attributes:
    _enabled: Boolean. Whether or not the PWM is enabled.
    _output_pin: DigitalOutput. The DigitalOutput GPIO pin being used for PWM.
    _duty_cycle. Float from 0.0 to 100.0. The current duty cycle as a percent.
    _frequency_hz: Float. The current PWM frequency in Hertz.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, output_pin):
    """Creates a PWM output.

    Args:
      output_pin: A DigitalOutput to use for PWM output.
    """
    self._enabled = False
    self._output_pin = output_pin
    self._duty_cycle = 0.0
    self._frequency_hz = 0.0

  @abc.abstractmethod
  def _enable(self):
    """Enables the PWM output.

    This method should be implemented by the platform.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def _disable(self):
    """Disables the PWM output.

    This method should be implemented by the platform.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def _set_duty_cycle(self, duty_cycle):
    """Sets the duty cycle of the PWM output.

    This method should be implemented by the platform.

    Args:
      duty_cycle: Float from 0.0 to 100.0. Duty cycle to set PWM output to.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def _set_frequency_hz(self, freqency_hz):
    """Sets the PWM frequency used for PWM output.

    This method should be implemented by the platform.

    Args:
      frequency_hz: Float. The frequency to set the PWM output to.
    """
    raise NotImplementedError

  def enable(self):
    """Enables the PWM output."""
    if not self._enabled:
      self._enable()
    self._enabled = True

  def disable(self):
    """Disables the PWM output."""
    if self._enabled:
      self._disable()
    self._enabled = False

  @property
  def is_enabled(self):
    """Checks if the PWM output is enabled.

    Returns:
      True if the PWM output is enabled, Flase otherwise.
    """
    return self._enabled

  @property
  def duty_cycle(self):
    """Gets the current value for the PWM output's duty cycle.

    Returns:
      The current duty cycle as a float.
    """
    return self._duty_cycle

  def set_duty_cycle(self, duty_cycle):
    """Sets the duty cycle of the PWM output.

    Args:
      duty_cycle: Float from 0.0 to 100.0. Duty cycle to set the PWM output to.

    Raises:
      ValueError: Thrown if duty_cycle is not between 0.0 and 100.0
    """
    if duty_cycle < 0 or duty_cycle > 100:
      raise ValueError('Duty cycle must be between 0 and 100. Got: %d'
                       % duty_cycle)
    self._set_duty_cycle(duty_cycle)
    self._duty_cycle = duty_cycle

  @property
  def frequency_hz(self):
    """Gets the current frequency used by the PWM output.

    Returns:
      The current frequency in Hertz as a float.
    """
    return self._frequency_hz

  def set_frequency_hz(self, frequency_hz):
    """Sets the PWM frequency used for PWM output.

    Args:
      frequency_hz: Float. The frequency to set the PWM output to.

    Raises:
      ValueError: Thrown if the frequency is negative.
    """
    if frequency_hz < 0:
      raise ValueError('Frequency must be greater than 0. Got: %d'
                       % frequency_hz)
    self._set_frequency_hz(frequency_hz)
    self._frequency_hz = frequency_hz

  @property
  def pin_number(self):
    """Gets the pin number of the PWM output.

    Returns:
      The pin number as an integer.
    """
    return self._output_pin.pin_number
