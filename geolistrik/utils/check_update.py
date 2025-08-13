import requests
from geolistrik.config import VERSION, REPO

CURRENT_VERSION = VERSION

def check_update():
    try:
        url = f"https://api.github.com/repos/{REPO}/releases/latest"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            latest = r.json()["tag_name"].lstrip("v")
            if latest != CURRENT_VERSION:
                print(f"⚠️  Update available: {latest} (current: {CURRENT_VERSION})")
                print(f"⬇️  Download: https://github.com/{REPO}/releases/latest")
    except Exception:
        pass