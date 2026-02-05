from geolistrik.domain.entities.measurement import Measurement
from geolistrik.domain.entities.electrode import Electrode

# optional electrode
def test_measurement_with_four_electrodes():
  m = Measurement(
    A=Electrode(0),
    B=Electrode(1),
    M=Electrode(2),
    N=Electrode(3),
    level=1,
    x_location=1.5
  )
  assert m.N is not None

def test_measurement_without_B_and_N():
  m = Measurement(
    A=Electrode(0),
    M=Electrode(2),
    level=1,
    x_location=1.5
  )
  assert m.B is None
  assert m.N is None