from abc import ABC, abstractmethod
from domain.entities.survey_line import SurveyLine
from domain.entities.array_result import ArrayResult

class ArrayConfiguration(ABC):
  @abstractmethod
  def generate(self, line: SurveyLine) ->ArrayResult:
    pass
  