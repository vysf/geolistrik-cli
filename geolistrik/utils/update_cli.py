import os
import sys
import platform
import requests
import tempfile
import subprocess
import shutil
from pathlib import Path

from geolistrik.config import VERSION, REPO

# Info repo
CURRENT_VERSION = VERSION  # Atau import dari config.py

def get_latest_release():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    r = requests.get(url, timeout=5)
    if r.status_code == 200:
        data = r.json()
        tag = data["tag_name"].lstrip("v")
        assets = data.get("assets", [])
        return tag, assets
    else:
        raise Exception(f"GitHub API error: {r.status_code}")

def download_file(url, dest_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

def update_cli():
    print("🔍 Checking for updates...")
    try:
        latest_version, assets = get_latest_release()

        if latest_version == CURRENT_VERSION:
            print(f"✅ Already up to date (v{CURRENT_VERSION})")
            return

        print(f"⚠️ Update available: v{latest_version} (current: v{CURRENT_VERSION})")

        system_os = platform.system()

        # Cari asset yang sesuai OS
        if system_os == "Windows":
            asset = next((a for a in assets if a["name"].endswith(".exe")), None)
            if not asset:
                print("❌ No Windows installer found in latest release.")
                return
            url = asset["browser_download_url"]
            temp_path = Path(tempfile.gettempdir()) / asset["name"]

            print(f"⬇️ Downloading installer to {temp_path} ...")
            download_file(url, temp_path)
            print("🚀 Running installer...")
            os.startfile(temp_path)  # Jalankan installer
            print("ℹ️ Please follow the installer to complete the update.")

        elif system_os == "Linux":
            asset = next((a for a in assets if "linux" in a["name"].lower()), None)
            if not asset:
                print("❌ No Linux binary found in latest release.")
                return
            url = asset["browser_download_url"]
            temp_path = Path(tempfile.gettempdir()) / asset["name"]

            print(f"⬇️ Downloading binary to {temp_path} ...")
            download_file(url, temp_path)

            dest_path = Path("/usr/local/bin/geolistrik")
            print(f"🔄 Replacing old binary at {dest_path} ...")
            subprocess.run(["sudo", "mv", str(temp_path), str(dest_path)])
            subprocess.run(["sudo", "chmod", "+x", str(dest_path)])
            print("✅ Update complete.")

        else:
            print(f"❌ OS {system_os} not supported for auto-update.")

    except Exception as e:
        print(f"❌ Update check failed: {e}")

# Contoh integrasi di CLI:
# if __name__ == "__main__":
#     if "--update" in sys.argv:
#         update_cli()
