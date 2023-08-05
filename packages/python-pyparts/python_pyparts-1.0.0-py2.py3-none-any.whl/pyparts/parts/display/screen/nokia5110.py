import time

from pyparts.parts import base_part

_LCD_WIDTH = 84
_LCD_HEIGHT = 48
_NUMBER_OF_LINES = 6
_PIXELS_PER_LINE = _LCD_HEIGHT / _NUMBER_OF_LINES
_POWER_DOWN = 0x04
_ENTRY_MODE = 0x02

_FUNCTION_SET = 0x20
_EXTENDED_INSTRUCTION = 0x01

_DISPLAY_CONTROL = 0x08
_DISPLAY_BLANK = 0x0
_DISPLAY_NORMAL = 0x4
_DISPLAY_ALL_ON = 0x1
_DISPLAY_INVERTED = 0x5

_SET_X_ADDR = 0x80
_SET_Y_ADDR = 0x40
_SET_VOP = 0x80
_SET_BIAS = 0x10
_SET_TEMP = 0x04


class Nokia5110(base_part.BasePart):

  def __init__(self, spi, dc, rst, led):
    """Creates a Nokia5110 display.

    Args:
      spi: SPI peripheral object to communicate with the display over.
      dc: Digital output. Used to toggle between data and command modes.
      rst: Digital output. Reset pin.
      led: LED object. Controls the backlight.
    """
    self._spi = spi
    self._spi.open()
    self._spi.set_mode(0)
    self._spi.set_clock_frequency(4000000)

    self._dc = dc
    self._rst = rst
    self._led = led
    self._enabled = False

  def __del__(self):
    self._spi.close()
    super(Nokia5110, self).__del__()

  def send_command(self, command):
    self._dc.set_low()
    self._spi.write([command])

  def send_extended_command(self, command):
    # Set extended command mode
    self.send_command(_FUNCTION_SET | _EXTENDED_INSTRUCTION)
    self.send_command(command)
    # Set normal display mode.
    self.send_command(_FUNCTION_SET)
    self.send_command(_DISPLAY_CONTROL | _DISPLAY_NORMAL)

  def send_data(self, data):
    self._dc.set_high()
    self._spi.write(data)

  def enable(self, contrast=50, bias=4):
    self.reset()
    self.set_bias(bias)
    self.set_contrast(contrast)
    self._enabled = True

  @property
  def is_enabled(self):
    return self._enabled

  def reset(self):
    self._rst.set_low()
    time.sleep(0.1)
    self._rst.set_high()

  def set_cursor(self, x, y):
    self.send_command(_SET_X_ADDR | x)
    self.send_command(_SET_Y_ADDR | y)

  def reset_cursor(self):
    self.set_cursor(0, 0)

  def display_image(self, image):
    if image.mode != '1':
      raise ValueError('Image must be in 1bit mode.')
    buffer = []
    pix = image.load()
    for row in range(_NUMBER_OF_LINES):
      for x in range(_LCD_WIDTH):
        bits = 0
        for bit in range(8):
          bits = bits << 1
          bits |= 1 if pix[(x, row * _PIXELS_PER_LINE + 7 - bit)] == 0 else 0
        buffer.append(bits)
    self.clear()
    self.send_data(buffer)


  def clear(self):
    self.reset_cursor()
    self.send_data([0] * (_LCD_WIDTH * _LCD_HEIGHT / 8))

  def set_contrast(self, contrast):
    contrast = max(0, min(contrast, 0x7f))
    self.send_extended_command(_SET_VOP | contrast)

  def set_bias(self, bias):
    self.send_extended_command(_SET_BIAS | bias)

  def set_backlight(self, duty_cycle):
    self._led.set_duty_cycle(duty_cycle)

  @property
  def height(self):
    return _LCD_HEIGHT

  @property
  def width(self):
    return _LCD_WIDTH

  @property
  def lines(self):
    return _NUMBER_OF_LINES
