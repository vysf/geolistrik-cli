from geolistrik.domain.arrays.dipole_dipole import DipoleDipole
from geolistrik.domain.entities.survey_line import SurveyLine

def test_dipole_dipole_basic_geometry():
  line = SurveyLine(0, 6, 1)
  config = DipoleDipole()

  result = config.generate(line)

  assert len(result.measurements) > 0
  m0 = result.measurements[0]

  assert m0.A.x == 0.0
  assert m0.B.x == 1.0
  assert m0.M.x == 2.0
  assert m0.N.x == 3.0
  assert m0.level == 1
