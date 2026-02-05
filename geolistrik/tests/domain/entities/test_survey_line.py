import pytest
from geolistrik.domain.entities.survey_line import SurveyLine
from geolistrik.domain.errors.invariant_error import InvariantError

def test_valid_survey_line():
  line = SurveyLine(0, 10, 2)
  assert line.x_start == 0.0
  assert line.x_end == 10
  assert line.spacing == 2

# invalid cases (invariant)
# tambah parameter `match` pada raises untuk mencocokan pesan error
def test_spacing_cannot_be_negative():
  with pytest.raises(InvariantError):
    assert SurveyLine(0, 10, -2)

def test_spacing_cannot_be_zero():
  with pytest.raises(InvariantError):
    assert SurveyLine(0, 10, 0)

def test_spacing_larger_than_line_length_is_invalid():
  with pytest.raises(InvariantError):
    assert SurveyLine(0, 10, 20)

def test_x_start_and_end_cannot_be_same():
  with pytest.raises(InvariantError):
    assert SurveyLine(10, 10, 2)

# direction test
def test_reverse_direction_allowed():
  line = SurveyLine(10, 0, 2)
  positions = line.positions()
  assert positions == [10, 8, 6, 4, 2, 0]