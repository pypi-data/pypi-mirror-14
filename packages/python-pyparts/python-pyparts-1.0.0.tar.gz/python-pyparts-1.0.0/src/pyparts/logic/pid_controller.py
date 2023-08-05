import time
import threading


class PIDController(object):
  """A PID controller for controlling output based on desired value.

  Attributes:
    _kp: Integer. The constant term.
    _ki: Integer. The integrator term.
    _kd: Integer. The differential term.
    _prev_error: Float. The error value from the previous calculation.
    _cp: Integer. Temp storage for constant term.
    _ci: Integer. Accumulator for integrator error value.
    _cd: Integer. Accumulator for differntial error value.
    _prev_time: Integer. The time of the previous calculation.
  """

  def __init__(self, kp, ki, kd):
    """Creates a PIDController.

    Args:
      kp: Integer. The constant term.
      ki: Integer. The integrator term.
      kd: Integer. The differential term.
    """
    self._kp = kp
    self._ki = ki
    self._kd = kd

    self._prev_error = 0
    self._cp = 0
    self._ci = 0
    self._cd = 0

    self._prev_time = time.time()

  def get_output(self, error):
    """Does a PID calculation and returns the new output value.

    Args:
      error: Float. The current error value.

    Returns:
      Float. The output of the PID controller for the current error.
    """
    self._current_time = time.time()
    dt = self._current_time - self._prev_time
    de = error - self._prev_error

    self._cp = self._kp * error
    self._ci += error * dt
    self._cd = 0
    if dt > 0:
      self._cd = de / dt

    self._prev_time = self._current_time
    self._prev_error = error

    return self._cp  + (self._ki * self._ci) + (self._kd * self._cd)

  class Worker(threading.Thread):
    """A worker for a PIDController to allow background processing.

    PIDController.Worker can be used to run a PID controller loop in a
    background thread. The worker calls the input function to get the current
    error value. It then computes the output value using the PID controller and
    calls the output function with that value.

    Attributes:
      _controller: PIDController. The PIDController used to calculate output
        values.
      _input_func: Function. Function called to determine error.
      _output_func: Function. Function called with the output of the PID.
      _set_point: Float. The desired value.
      _stop: Boolean. Set to true to disable the controller.
    """

    def __init__(self, kp, kd, ki, input_func, output_func):
      """Creates a PIDController.Worker.

      Args:
        kp: Integer. The constant term.
        ki: Integer. The integrator term.
        kd: Integer. The differential term.
        input_func: Function. Function called to calculate error.
        output_func: Function. Function called with the output of the PID.
      """
      super(PIDController.Worker, self).__init__()
      self._controller = PIDController(kp, ki, kd)
      self._input_func = input_func
      self._output_func = output_func
      self._set_point = 0
      self._stop = False

    @property
    def desired_value(self):
      """Gets the current desired value.

      Returns:
        Float. The current desired value.
      """
      return self._set_point

    def set_desired_value(self, value):
      """Sets the desired output value.

      Args:
        value: Float. The value to try and achieve.
      """
      self._set_point = value

    def stop(self):
      """Stops the controller."""
      self._stop = True

    def run(self):
      """Loop for calculating error, running the PID, and handling output."""
      while not self._stop:
        current_val = self._input_func()
        error = self._set_point - current_val
        self._output_func(self._controller.get_output(error))
