from dataclasses import dataclass
from geolistrik.domain.errors.invariant_error import InvariantError

@dataclass(frozen=True)
class Electrode:
  x: float

  def __post_init__(self):
    if not isinstance(self.x, (int, float)):
      raise InvariantError("Electrode.x must be numeric")

    # karena frozen=True, pakai object.__setattr__
    object.__setattr__(self, "x", float(self.x))