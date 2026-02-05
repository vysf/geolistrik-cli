# InvariantError (aturan internal domain)
# Dipakai untuk:
# - spacing negatif
# - lintasan invalid
# - elektroda overlap
# - dll
from geolistrik.domain.errors.base import GeolistrikError

class InvariantError(GeolistrikError):
  pass