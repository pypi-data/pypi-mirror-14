from pyparts.parts.sensor.temperature import base_temperature_sensor

_INTERNAL_TEMP_MASK = 0xfff0
_INTERNAL_TEMP_SHIFT = 4
_INTERNAL_TEMP_MSB_MASK = 0x800
_INTERNAL_DEGREES_C_PER_BIT = 0.0625

_THERMOCOUPLE_TEMP_MASK = 0xfffe0000
_THERMOCOUPLE_TEMP_SHIFT = 18
_THERMOCOUPLE_TEMP_MSB_MASK = 0x2000
_THERMOCOUPLE_DEGREES_C_PER_BIT = 0.25

_FAULT_BIT_MASK = 0x8000


class MAX31855(base_temperature_sensor.BaseTemperatureSensor):

  def __init__(self, spi_bus):
    super(MAX31855, self).__init__()
    self._spi_bus = spi_bus
    self._spi_bus.open()
    self._spi_bus.set_mode(0)

  def __del__(self):
    self._spi_bus.close()
    super(MAX31855, self).__del__()

  def _get_temp_c(self):
    value = self._read()
    value &= _THERMOCOUPLE_TEMP_MASK
    value >>= _THERMOCOUPLE_TEMP_SHIFT
    if value & _THERMOCOUPLE_TEMP_MSB_MASK:
      value -= 16384
    return value * _THERMOCOUPLE_DEGREES_C_PER_BIT

  @property
  def internal_temp_c(self):
    value = self._read()
    value &= _INTERNAL_TEMP_MASK
    value >>= _INTERNAL_TEMP_SHIFT
    if value & _INTERNAL_TEMP_MSB_MASK:
      value -= 4096
    return value * _INTERNAL_DEGREES_C_PER_BIT

  @property
  def internal_temp_f(self):
    return self._to_f(self.get_internal_temp_c())

  def _read(self):
    values = self._spi_bus.read(4)
    if not values or len(values) != 4:
      raise RuntimeError('Unable to read MAX31855 data.')
    packed_value = (values[0] << 24 | values[1] << 16 |
                    values[2] << 8 | values[3])
    if packed_value & _FAULT_BIT_MASK:
      raise RuntimeError('MAX31855 error. Fault bit set.')
    return packed_value
