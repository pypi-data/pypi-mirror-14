import abc

# Pin values
HIGH = True
LOW = False


class GPIOError(Exception):
  """Error type for exceptions while writing to GPIO pins."""
  pass


class BaseGPIO(object):
  """A class for creating GPIO type peripherals.

  BaseGPIO implements basic GPIO functionality such as reading pin values
  and setting pins high or low. Platforms are expected to subclass BaseGPIO
  and provide platform specific implementations of _write and _read. Platforms
  will likely also have to override the constructor to do platform specific
  initialization tasks like setting the pin to INPUT or OUTPUT.
  
  Attributes:
    _pin: The GPIO pin being used. For example a pin number.
    _mode: The mode the pin is in. For example INPUT or OUTPUT.
  """
  __metaclass__ = abc.ABCMeta

  # Pin modes
  OUTPUT = 0
  INPUT = 1
  BIDIRECTIONAL = 2

  # Internal resistor configurations
  PUD_UP = 1
  PUD_DOWN = 2

  def __init__(self, pin, mode, pull_up_down):
    """Creates a GPIO pin.

    Args:
      pin: Integer. The pin to create the GPIO on.
      mode: INPUT, OUTPUT, or BIDIRECTIONAL. The type of pin mode to use.
      pull_up_down: PUD_UP or PUD_DOWN. Enable pull up or pull down resistors.
    """
    self._pin = pin
    self._mode = mode
    self._pull_up_down = pull_up_down

  @abc.abstractmethod
  def _write(self, value):
    """Writes a value to the pin.

    This method should be implemented by the platform.

    Args:
      value: The value to write to the pin.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def _read(self):
    """Reads the current value of a pin.

    This method should be implemented by the platform.

    Returns:
      The GPIO pin's current value as HIGH or LOW.
    """
    raise NotImplementedError

  @property
  def pin_number(self):
    """Gets the pin number of the GPIO.

    Returns:
      The GPIO's pin number.
    """
    return self._pin

  @property
  def mode(self):
    """Gets the mode the GPIO pin is in.

    Returns:
      The mode being used by the GPIO pin.
    """
    return self._mode

  @property
  def pull_up_down(self):
    """Gets the state of the GPIO pull up or pull down resistors.

    Returns:
      The state of the GPIO pull up or pull down resistors.
    """
    return self._pull_up_down

  def set_high(self):
    """Writes a value of HIGH to the GPIO pin.

    Raises:
      GPIOError: Trying to write to a pin in INPUT mode will throw an
        exception.
    """
    if self._mode == self.INPUT:
      raise GPIOError('Failed to write pin %d high. Pin %d is an input.'
                      % (self._pin, self._pin))
    self._write(HIGH)

  @property
  def is_high(self):
    """Checks if the GPIO pin has a value of HIGH.

    Returns:
      True if the pin is in a HIGH state, False otherwise.
    """
    return self._read() == HIGH

  def set_low(self):
    """Writes a value of LOW to the GPIO pin.

    Raises:
      GPIOError: Trying to write to a pin in INPUT mode will throw an
        exception.
    """
    if self._mode == self.INPUT:
      raise GPIOError('Failed to write pin %d low. Pin %d is an input.'
                      % (self._pin, self._pin))
    self._write(LOW)

  @property
  def is_low(self):
    """Checks if the GPIO pin has a value of LOW.

    Returns:
      True if the GPIO pin is in a LOW state, False otherwise.
    """
    return self._read() == LOW


class BaseDigitalInput(BaseGPIO):
  """A class for creating digital input type peripherals.

  BaseDigitalInput adds interrupt functionality to BaseGPIO.
  """

  # Platforms should implement these
  INTERRUPT_FALLING = None
  INTERRUPT_RISING = None
  INTERRUPT_BOTH = None

  @abc.abstractmethod
  def add_interrupt(self, type, callback=None, debounce_time_ms=0):
    """Adds an interrupt to the digital input pin.

    Args:
      type: FALLING, RISING, or BOTH. Edge to trigger the interrupt on.
      callback: Function. The function to call when the interrupt fires.
          (default=None)
      debounce_time_ms: Integer. Debounce time to put on the interrupt.
          (default=0)
    """
    raise NotImplementedError

  @abc.abstractmethod
  def wait_for_edge(self, type):
    """Blocks until the edge is detected.

    Args:
      type: RISING, FALLING, or BOTH. Edge to detect before unblocking.
    """
    raise NotImplementedError

  def remove_interrupt(self):
    """Removes all interrupts from the digital input pin."""
    raise NotImplementedError
