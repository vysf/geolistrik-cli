import pytest
from geolistrik.domain.entities.electrode import Electrode

def test_electrode_accepts_float():
  e = Electrode(10.5)
  assert e.x == 10.5

def test_electrode_casts_int_to_float():
  e = Electrode(10)
  assert isinstance(e.x, float)

def test_electrode_rejects_non_numeric():
  with pytest.raises(TypeError):
    Electrode("10")