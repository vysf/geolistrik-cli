import os
import sys
import platform
import requests
import tempfile
import subprocess
import shutil
from urllib.request import urlretrieve

from geolistrik.config import REPO, APP_NAME, VERSION as CURRENT_VERSION


def get_latest_version():
    """Get latest version from GitHub"""
    api_url = f"https://api.github.com/repos/{REPO}/releases/latest"
    response = requests.get(api_url, timeout=5)
    response.raise_for_status()
    return response.json()["tag_name"].lstrip("v")

def download_file(url, dest_path):
    """Download from url to dest_path"""
    print(f"📥 Downloading from {url} ...")
    urlretrieve(url, dest_path)
    print(f"📥 File successfully downloaded to {dest_path}")

def update_windows(latest_version):
    """CLI update on Windows"""
    download_url = f"https://github.com/{REPO}/releases/download/v{latest_version}/geolistriksetup-{latest_version}.exe"
    temp_dir = tempfile.gettempdir()
    installer_path = os.path.join(temp_dir, f"geolistriksetup-{latest_version}.exe")

    download_file(download_url, installer_path)

    print("🚀 Running installer...")
    print("ℹ️ Please follow the installer to complete the update.")
    subprocess.run([installer_path], check=True)

def update_linux(latest_version):
    """CLI update on Linux"""

    # make sure the script run with sudo
    if os.geteuid() != 0:
        print("⚠️ Run this command with sudo:")
        print("   sudo geolistrik --update")
        sys.exit(1)

    download_url = f"https://github.com/{REPO}/releases/download/v{latest_version}/geolistrik-linux-{latest_version}.bin"
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, f"geolistrik-linux-{latest_version}.bin")

    download_file(download_url, temp_file_path)

    dest_path = "/usr/local/bin/geolistrik"
    print(f"🔄 Updating {APP_NAME} in {dest_path} ...")
    shutil.move(temp_file_path, dest_path)
    os.chmod(dest_path, 0o755)

    print("✅ Update successfully")

def update_cli():
    print("🔍 Checking for updates...")
    try:
        latest_version = get_latest_version()
    except Exception as e:
        print(f"❌ Failed to check for latest version: {e}")
        sys.exit(1)
    

    if latest_version == CURRENT_VERSION:
        print(f"✅ Already up to date (v{CURRENT_VERSION})")
        return

    print(f"⚠️  Update available: v{latest_version} (current: v{CURRENT_VERSION})")
    
    os_name = platform.system()
    if os_name == "Windows":
        update_windows(latest_version)
    elif os_name == "Linux":
        update_linux(latest_version)
    else:
        print(f"❌ OS {system_os} not supported for auto-update.")
    