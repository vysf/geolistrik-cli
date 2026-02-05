from abc import ABC, abstractmethod
from geolistrik.domain.entities.survey_line import SurveyLine
from geolistrik.domain.entities.array_result import ArrayResult

class ArrayConfiguration(ABC):
  @abstractmethod
  def generate(self, line: SurveyLine) ->ArrayResult:
    pass # pragma: no cover
  