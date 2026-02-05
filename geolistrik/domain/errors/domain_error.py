# DomainError (logic gagal, tapi input valid)
# Contoh:
# tidak cukup elektroda untuk konfigurasi tertentu
# survey terlalu pendek untuk n-level

from geolistrik.domain.errors.base import GeolistrikError

class DomainError(GeolistrikError):
  pass