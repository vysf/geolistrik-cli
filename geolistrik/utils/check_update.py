import requests
from geolistrik.config import REPO, VERSION as CURRENT_VERSION

def check_update():
    api_url = f"https://api.github.com/repos/{REPO}/releases/latest"
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()
    latest_version = response.json()["tag_name"].lstrip("v")

    if latest_version != CURRENT_VERSION:
        print(f"⚠️  Update available: v{latest_version} (current: v{CURRENT_VERSION})")
        print(f"⬇️  Download: {api_url}")
        