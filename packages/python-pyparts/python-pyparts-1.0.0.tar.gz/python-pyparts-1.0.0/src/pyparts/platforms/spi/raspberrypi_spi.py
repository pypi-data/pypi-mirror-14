import spidev

from pyparts.platforms.spi import base_spi


class RaspberryPiHardwareSPIBus(base_spi.BaseHardwareSPIBus):
  """Raspberry Pi implementation of a hardware SPI bus.

  Attributes:
    _spi_device: The SPI device used for reading and writing.
  """

  def __init__(self, port, device):
    """Creates a RaspberryPiHardwareSPIBus.
    
    Args:
      port: Integer. The port to use for the SPI bus.
      device: Integer. The device to use for the SPI bus.
    """
    super(RaspberryPiHardwareSPIBus, self).__init__(port, device)
    self._spi_device = spidev.SpiDev()

  def _open(self):
    """Opens the SPI bus."""
    self._spi_device.open(self._port, self._device)

  def _close(self):
    """Closes the SPI bus."""
    self._spi_device.close()

  def _set_clock_frequency_hz(self, frequency_hz):
    """Sets the clock freqency used by the SPI bus.

    Args:
      freqency_hz: Float. The frequency to set the SPI bus clock to.
    """
    self._spi_device.max_speed_hz = frequency_hz

  def _set_mode(self, mode):
    """Sets the SPI bus mode.

    Args:
      mode: Integer between 0 and 3. The mode to set the SPI bus to.
    """
    self._spi_device.mode = mode

  def _set_bit_order(self, order):
    """Sets the SPI bus bit order.

    Args:
      order: MSB_FIRST or LSB_FIRST. The bit order to set the SPI bus to.
    """
    self._spi_device.lsbfirst = order == self.LSB_FIRST

  def write(self, data):
    """Writes data to the SPI bus.

    Args:
      data: Bytearray. Data to write over the SPI bus.
    """
    self._spi_device.writebytes(data)

  def read(self, length):
    """Reads at most length bytes from the SPI bus.

    Args:
      length: Integer. The maximum number of bytes to read from the SPI bus.

    Returns:
      A bytearray of the bytes read from the bus.
    """
    return bytearray(self._spi_device.readbytes(length))
