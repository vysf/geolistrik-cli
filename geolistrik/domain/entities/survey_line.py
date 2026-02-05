from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class SurveyLine:
  x_start: float
  x_end: float
  spacing: float

  def __post_init__(self):
    x_start = float(self.x_start)
    x_end = float(self.x_end)
    spacing = float(self.spacing)

    if x_start == x_end:
        raise ValueError("x_start and x_end must be different")

    if spacing <= 0:
        raise ValueError("spacing must be > 0")

    if spacing >= abs(x_end - x_start):
        raise ValueError("spacing must be smaller than line length")

    object.__setattr__(self, "x_start", x_start)
    object.__setattr__(self, "x_end", x_end)
    object.__setattr__(self, "spacing", spacing)

  def positions(self) -> list[float]:
    direction = 1 if self.x_end > self.x_start else -1
    length = abs(self.x_end - self.x_start)

    step = Decimal(str(self.spacing))
    start = Decimal(str(self.x_start))

    count = int(length / step) + 1

    return [
        float(start + direction * i * step)
        for i in range(count)
    ]