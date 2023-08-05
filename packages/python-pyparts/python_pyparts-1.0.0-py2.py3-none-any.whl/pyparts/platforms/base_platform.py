import abc


class BasePlatform(object):
  """An abstract class for creating platforms.

  BasePlatform is what all platforms are created from. Platforms are expected
  to override the methods of BasePlatform to provide different kinds of
  peripheral devices like GPIO pins, PWM pins, and communication busses.
  """
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def get_digital_input(self, pin):
    raise NotImplementedError

  @abc.abstractmethod
  def get_digital_output(self, pin):
    raise NotImplementedError

  @abc.abstractmethod
  def get_pwm_output(self, pin):
    raise NotImplementedError

  @abc.abstractmethod
  def get_hardware_spi_bus(self, port, device):
    raise NotImplementedError

  @abc.abstractmethod
  def get_software_spi_bus(self, sclk_pin, mosi_pin, miso_pin, ss_pin):
    raise NotImplementedError

  @abc.abstractmethod
  def get_i2c_bus(self):
    raise NotImplementedError
