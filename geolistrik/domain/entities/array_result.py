from dataclasses import dataclass
from geolistrik.domain.entities.survey_line import SurveyLine
from geolistrik.domain.entities.measurement import Measurement
from geolistrik.domain.entities.electrode import Electrode

@dataclass(frozen=True)
class ArrayResult:
  array_type: str
  survey_line: SurveyLine
  measurements: list[Measurement]
  electrode_positions: list[Electrode]