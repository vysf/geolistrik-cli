from geolistrik.domain.entities.array_result import ArrayResult
from geolistrik.domain.entities.survey_line import SurveyLine

def test_array_result_holds_measurements():
  line = SurveyLine(0, 10, 2)
  result = ArrayResult(
    array_type="",
    survey_line=line, 
    measurements=[],
    electrode_positions=[]
  )
  assert result.survey_line == line
  assert isinstance(result.measurements, list)