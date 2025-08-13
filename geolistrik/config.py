import os
from dotenv import load_dotenv

# Load .env hanya jika ada
load_dotenv()

APP_NAME = "Geolistrik CLI"

# Ambil versi dengan urutan prioritas: .env > GitHub Actions env > default
VERSION = (
    os.environ.get("GEOLISTRIK_VERSION") or
    os.environ.get("VERSION") or
    "dev"
)

AUTHOR = "Yusuf Umar Al Hakim"
CONTACT = "yusufumaralhakim@fmipa.untan.ac.id"

# Ambil repo (format: username/repo) dengan urutan prioritas sama
REPO = (
    os.environ.get("GEOLISTRIK_REPO") or
    os.environ.get("REPO") or
    "vysf/geolistrik-cli"
)

# URL website otomatis dari REPO
WEBSITE = f"https://github.com/{REPO}"
