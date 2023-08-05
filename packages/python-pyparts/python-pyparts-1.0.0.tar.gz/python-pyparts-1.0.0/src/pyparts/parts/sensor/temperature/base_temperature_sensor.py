import abc

from pyparts.parts import base_part


class BaseTemperatureSensor(base_part.BasePart):
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def _get_temp_c(self):
    raise NotImplementedError

  @property
  def temp_c(self):
    return self._get_temp_c()

  @property
  def temp_f(self):
    return self._to_f(self.temp_c)

  def _to_f(self, temp):
    return (temp * 9 / 5) + 32
