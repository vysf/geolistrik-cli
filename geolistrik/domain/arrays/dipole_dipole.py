from domain.arrays.base import ArrayConfiguration
from domain.entities.array_result import ArrayResult
from domain.entities.measurement import Measurement
from domain.entities.electrode import Electrode
from domain.entities.survey_line import SurveyLine

class DipoleDipole(ArrayConfiguration):

  def generate(self, line: SurveyLine) -> ArrayResult:
    positions = line.positions()
    electrodes = [Electrode(x) for x in positions]
    measurements: list[Measurement] = []

    n = 1
    while True:
      created = False
      for i in range(len(electrodes)):
        try:
          A = Electrode(positions[i])
          B = Electrode(positions[i + 1])
          M = Electrode(positions[i + 1 + n])
          N = Electrode(positions[i + 2 + n])
        except:
          break

        x_loc = (M.x + N.x) / 2.0

        measurements.append(
            Measurement(
              A=A,
              B=B,
              M=M,
              N=N,
              level=n,
              x_location=x_loc
            )
        )
        created = True

      if not created:
          break
      n += 1

    return ArrayResult(
      array_type="dipole-dipole",
      survey_line=line,
      measurements=measurements,
      electrode_positions=electrodes
    )
