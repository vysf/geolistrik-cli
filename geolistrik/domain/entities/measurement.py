from dataclasses import dataclass
from typing import Optional
from geolistrik.domain.entities.electrode import Electrode

@dataclass(frozen=True)
class Measurement:
  A: Electrode
  M: Electrode
  B: Optional[Electrode] = None
  N: Optional[Electrode] = None
  level: int = 1
  x_location: float = 0.0