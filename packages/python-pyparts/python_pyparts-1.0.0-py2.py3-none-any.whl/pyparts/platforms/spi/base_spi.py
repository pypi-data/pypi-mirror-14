import abc

class BaseSPIBus(object):
  """A class for creating SPI bus peripherals.
  
  BaseSPIBus implements methods to interact with an SPI peripheral. Platforms
  are expected to subclass BaseSPIBus and provide platform specific
  implementations of _open, _close, _set_clock_frequency_hz, _set_mode,
  _set_bit_order, write, and read.

  Attributes:
    _is_open: Boolean. Whether or not the SPI bus is open.
    _clock_frequency_hz: Float. The SPI bus clock frequency.
    _mode: Integer between 0 and 3. The SPI bus mode.
    _bit_order: MSB_FIRST or LSB_FIRST. The bit order of the SPI bus.
  """
  __metaclass__ = abc.ABCMeta

  MSB_FIRST = 0
  LSB_FIRST = 1

  def __init__(self):
    """Creates an SPI bus."""
    self._is_open = False
    self._clock_frequency_hz = 0.0
    self._mode = 0
    self._bit_order = self.MSB_FIRST

  @abc.abstractmethod
  def _open(self):
    """Opens the SPI bus.
    
    This method should be implemented by the platform.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def _close(self):
    """Closes the SPI bus.
    
    This method should be implemented by the platform.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def _set_clock_frequency_hz(self, frequency_hz):
    """Sets the SPI bus clock frequency.
    
    This method should be implemented by the platform.

    Args:
      frequency_hz: Integer. Frequency to set the clock to.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def _set_mode(self, mode):
    """Sets the SPI bus mode..

    This method should be implemented by the platform.

    Args:
      mode: Integer between 0 and 3. The mode to set the SPI bus to.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def _set_bit_order(self, order):
    """Sets the SPI bus bit order.

    This method should be implemented by the platform.

    Args:
      order: MSB_FIRST or LSB_FIRST. The bit order to use for the SPI bus.
    """
    raise NotImplementedError

  def open(self):
    """Opens the SPI bus."""
    if not self._is_open:
      self._open()
    self._is_open = True

  def close(self):
    """Closes the SPI bus."""
    if self._is_open:
      self._close()
    self._is_open = False

  @property
  def is_open(self):
    """Checks if the SPI bus is open or not.

    Returns:
      True if the SPI bus is open, False otherwise.
    """
    return self._is_open

  @property
  def clock_frequency_hz(self):
    """Returns the current SPI bus clock frequency.
    
    Returns:
      The current SPI bus clock frequency as a float.
    """
    return self._clock_frequency_hz

  def set_clock_frequency_hz(self, frequency_hz):
    """Sets the clock freqency used by the SPI bus.

    Args:
      freqency_hz: Float. The frequency to set the SPI bus clock to.

    Raises:
      ValueError: Thrown if the frequency is less than 0.
      RuntimeError: Thrown if the bus isn't open.
    """
    if frequency_hz < 0:
      raise ValueError('Frequency must be greater than 0. Got %g'
                       % (frequency_hz))
    if not self._is_open:
      raise RuntimeError('SPI device must be opened before setting frequency.')
    self._set_clock_frequency_hz(frequency_hz)
    self._clock_frequency_hz = frequency_hz

  @property
  def mode(self):
    """Returns the current SPI bus mode.

    Returns:
      The current SPI bus mode as an integer.
    """
    return self._mode

  def set_mode(self, mode):
    """Sets the SPI bus mode.

    Args:
      mode: Integer between 0 and 3. The mode to set the SPI bus to.

    Raises:
      ValueError: Thrown if the mode is not between 0 and 3.
      RuntimeError: Thrown if the bus isn't open.
    """
    if mode < 0 or mode > 3:
      raise ValueError('Mode must be between 0 and 3. Got %d' % mode)
    if not self._is_open:
      raise RuntimeError('SPI device must be opened before setting mode.')
    self._set_mode(mode)
    self._mode = mode

  @property
  def bit_order(self):
    return self._bit_order

  def set_bit_order(self, order):
    """Sets the SPI bus bit order.

    Args:
      order: MSB_FIRST or LSB_FIRST. The bit order to set the SPI bus to.

    Raises:
      ValueError: Thrown if the order is not one of MSB_FIRST or LSB_FIRST.
      RuntimeError: Thrown if the bus isn't open.
    """
    if order not in (self.MSB_FIRST, self.LSB_FIRST):
      raise ValueError('Bit order must be MSB_FIRST or LSB_FIRST')
    if not self._is_open:
      raise RuntimeError('SPI device must be opened before setting bit order.')
    self._set_bit_order(order)
    self._bit_order = order

  @abc.abstractmethod
  def write(self, data):
    """Writes data to the SPI bus.

    This method should be implemented by the platform.

    Args:
      data: Bytearray. Data to write over the SPI bus.
    """
    raise NotImplementedError

  @abc.abstractmethod
  def read(self, length):
    """Reads at most length bytes from the SPI bus.

    This method should be implemented by the platform.

    Args:
      length: Integer. The maximum number of bytes to read from the SPI bus.
    """
    raise NotImplementedError


class BaseHardwareSPIBus(BaseSPIBus):
  """A class for creating SPI buses using hardware peripherals.

  BaseHardwareSPIBus implements methods to interact with hardware
  implementations of SPI buses.

  Attributes:
    _port: The SPI device port number.
    _device: The SPI device used for the bus.
  """

  def __init__(self, port, device):
    """Creates a BaseHardwareSPIBus.
    
    Args:
      port: Integer. The port to use for the SPI bus.
      device: Integer. The device to use for the SPI bus.
    """
    super(BaseHardwareSPIBus, self).__init__()
    self._port = port
    self._device = device

  @property
  def port(self):
    """Gets the SPI device port.

    Returns:
      The current port used by the SPI bus.
    """
    return self._port

  @property
  def device(self):
    """Gets the current SPI bus device.

    Returns:
      The current SPI bus device.
    """
    return self._device
