import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

APP_NAME = "Geolistrik CLI"
VERSION = os.environ.get("GEOLISTRIK_VERSION", "dev") 
AUTHOR = "Yusuf Umar Al Hakim"
CONTACT = "yusufumaralhakim@fmipa.untan.ac.id"
WEBSITE = f"https://github.com/{os.environ.get("GEOLISTRIK_REPO", "vysf")}"
REPO = {os.environ.get("GEOLISTRIK_REPO", "vysf")}
