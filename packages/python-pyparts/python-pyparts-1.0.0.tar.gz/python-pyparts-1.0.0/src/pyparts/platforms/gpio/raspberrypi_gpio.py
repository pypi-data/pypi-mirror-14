import RPi.GPIO as rpi_gpio

from pyparts.platforms.gpio import base_gpio


class RaspberryPiGPIO(base_gpio.BaseGPIO):
  """Raspberry Pi implementation of a GPIO peripheral."""

  def __init__(self, pin, mode, pull_up_down=base_gpio.BaseGPIO.PUD_UP):
    """Creates a GPIO pin for a Raspberry Pi.

    Args:
      pin: Integer. The pin number to create the GPIO on.
      mode: INPUT or OUTPUT. The pin mode to put the GPIO in.
      pull_up_down: PUD_UP or PUD_DOWN. Enable pull up or pull down resistors.
          (default=PUD_UP)
    """
    super(RaspberryPiGPIO, self).__init__(pin, mode, pull_up_down)
    
    if self._mode == self.INPUT:
      pin_type = rpi_gpio.IN
    else:
      pin_type = rpi_gpio.OUT

    if pull_up_down == self.PUD_UP:
      pud = rpi_gpio.PUD_UP
    else:
      pud = rpi_gpio.PUD_DOWN
    
    rpi_gpio.setup(self._pin, pin_type, pull_up_down=pud)
    
  def _write(self, value):
    """Writes a value to the pin.

    Args:
      value: HIGH or LOW. The value to write to the pin.
    """
    rpi_gpio.output(self._pin, value)

  def _read(self):
    """Reads the current value from the pin.

    Returns:
      The GPIO pin's current value as HIGH or LOW.
    """
    return rpi_gpio.input(self._pin)


class RaspberryPiDigitalInput(base_gpio.BaseDigitalInput, RaspberryPiGPIO):
  """Raspberry Pi implementation of a DigitalInput."""

  INTERRUPT_FALLING = rpi_gpio.FALLING
  INTERRUPT_RISING = rpi_gpio.RISING
  INTERRUPT_BOTH = rpi_gpio.BOTH

  def __init__(self, pin):
    """Creates a DigitalInput pin for a Raspberry Pi.

    Args:
      pin: Integer. The pin to create the DigitalInput on.
    """
    super(RaspberryPiDigitalInput, self).__init__(pin, self.INPUT)

  def add_interrupt(self, type, callback=None, debounce_time_ms=0):
    """Creates an interrupt on the digital input pin.

    Args:
      type: FALLING, RISING, or BOTH. Edge type to trigger the interrupt on.
      callback. Function. The function to call when the interrupt fires.
          (default=None)
      debounce_time_ms: Integer. Debounce time to add to the interrupt.
          (default=0)
    """
    rpi_gpio.add_event_detect(self._pin, type, callback, debounce_time_ms)

  def wait_for_edge(self, type):
    """Block until an edge is detected.

    Args:
      type: FALLING, RISING, or BOTH. Edge type to detect before unblocking.
    """
    rpi_gpio.wait_for_edge(self._pin, type)

  def remove_interrupt(self):
    """Removes all interrupts from the pin."""
    rpi_gpio.remove_event_detection(self._pin)


class RaspberryPiDigitalOutput(RaspberryPiGPIO):
  """Raspberry Pi implementation of a DigitalOutput."""

  def __init__(self, pin):
    """Creates a DigitalOutput pin for a Raspberry Pi.

    Args:
      pin: Integer. The pin to create the DigitalOutput on.
    """
    super(RaspberryPiDigitalOutput, self).__init__(pin, base_gpio.BaseGPIO.OUTPUT)
