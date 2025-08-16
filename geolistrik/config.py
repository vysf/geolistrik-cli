import os
from dotenv import load_dotenv

# Load .env hanya jika ada
load_dotenv()

APP_NAME = "Geolistrik CLI"

# Ambil versi dengan urutan prioritas: .env > GitHub Actions env > default
# SELAU UBAH VERSI SETIAP AKAN RELEASE
VERSION = os.getenv("GEOLISTRIK_VERSION", "1.0.0")

AUTHOR = "Yusuf Umar Al Hakim"
CONTACT = "yusufumaralhakim@fmipa.untan.ac.id"

# Ambil repo (format: username/repo) dengan urutan prioritas sama
REPO = os.getenv("GEOLISTRIK_REPO", "vysf/geolistrik-cli")

# URL website otomatis dari REPO
WEBSITE = f"https://github.com/{REPO}"
