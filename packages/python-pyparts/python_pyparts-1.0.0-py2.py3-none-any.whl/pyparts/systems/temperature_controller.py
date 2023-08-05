import time

from pyparts.logic import pid_controller


class TemperatureController(object):
  """A PID based temperature controller.

  TemperatureController uses a PID controller to regulate temperature.
  A temperature sensor is used to read the current temperature and a PWM based
  heater is used to increase the temperature when needed. Once the desired
  temperature is reached the heater turns off until the temperature falls below
  the desired temperature.

  Attributes:
    _temp_sensor: TemperatureSensor. A temperature sensor to read temperature
      values from.
    _heater_pin: PwmOutput. A PWM output that controls a heating element.
    _pid_worker: PIDController.Worker. Worker thread for maintaining a
      temperature.
  """

  # Error value at which PWM output will be set to 100%
  MAX_ERROR_DEGREES_C = 10.0

  def __init__(self, temp_sensor, heater_pin, kp, ki, kd):
    """Creates a TemperatureController.

    Args:
      temp_sensor: TemperatureSensor. A temperature sensor to read temperature.
      heater_pin: PwmOutput. A PWM output that controls a heating element.
      kp: Integer. PID controller constant term.
      ki: Integer. PID controller integrator term.
      kd: Integer. PID controller differentiator term.
    """
    self._temp_sensor = temp_sensor
    self._heater_pin = heater_pin
    self._pid_worker = pid_controller.PIDController.Worker(
        kp, ki, kd, self._pid_input_func, self._pid_output_func)
    self._is_enabled = False

  def _pid_input_func(self):
    """Input function to the PID controller."""
    return self._temp_sensor.temp_c

  def _pid_output_func(self, val):
    """Output function to handle PID controller error values.
    
    Args:
      val: Float. The output value from the PID controller.
    """
    # If the sensor is too hot, turn off the heater
    if val <= 0:
      self._heater_pin.set_duty_cycle(0)
      return
    if val > self.MAX_ERROR_DEGREES_C:
      self._heater_pin.set_duty_cycle(100)
      return
    self._heater_pin.set_duty_cycle(
        (float(val) / self.MAX_ERROR_DEGREES_C) * 100)
    time.sleep(1)

  def set_temp_c(self, temp_c):
    """Set the desired temerature value.

    Args:
      temp_c: Integer. The temperature to target with the controller.
    """
    self._pid_worker.desired_value = temp

  @property
  def temp_setting(self):
    """Get the current temperature set point."""
    return self._pid_worker.desired_value

  def enable(self):
    """Enable the temperature sensor and begin controlling the temperature."""
    if not self._is_enabled:
      self._pid_worker.start()
    self._is_enabled = True

  def disable(self):
    """Stops the temperature sensor and stops controlling the temperature."""
    if self._is_enabled:
      self._pid_worker.stop()
    self._is_enabled = False

  @property
  def is_enabled(self):
    """Checks whether the temperature controller has been enabled or not.

    Returns:
      Boolean. True if the controller has been started.
    """
    return self._is_enabled
