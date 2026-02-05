import pytest
from geolistrik.domain.arrays.base import ArrayConfiguration
from geolistrik.domain.arrays.dipole_dipole import DipoleDipole
from geolistrik.domain.entities.survey_line import SurveyLine
from geolistrik.domain.entities.array_result import ArrayResult

def test_array_configuration_is_abstract():
    with pytest.raises(TypeError):
        ArrayConfiguration()

def test_array_returns_array_result():
  line = SurveyLine(0, 10, 2)
  config = DipoleDipole()
  result = config.generate(line)

  assert isinstance(result, ArrayResult)
  assert result.survey_line == line


class BrokenArray(ArrayConfiguration):
  pass

def test_missing_generate_method_raises_error():
  with pytest.raises(TypeError):
    BrokenArray()


def run_array(config, line):
  return config.generate(line)

def test_array_polymorphism():
  line = SurveyLine(0, 10, 2)
  config = DipoleDipole()

  result = run_array(config, line)

  assert isinstance(result, ArrayResult)
  