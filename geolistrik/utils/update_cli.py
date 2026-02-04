import os
import sys
import time
import shutil
import platform
import requests
import tempfile
import subprocess

from rich.console import Console
from rich.progress import Progress, BarColumn, DownloadColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn

from geolistrik.config import REPO, APP_NAME, VERSION as CURRENT_VERSION

console = Console()

def _fetch_github_release_tag(tag=None, retries=3, delay=2):
    """Helper function to fetch release data from GitHub"""
    if tag:
        api_url = f"https://api.github.com/repos/{REPO}/releases/tags/v{tag}"
    else:
        api_url = f"https://api.github.com/repos/{REPO}/releases/latest"

    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(api_url, timeout=5)

            if response.status_code == 404:
                console.print(f"[red]Version '{tag}' not found in GitHub releases.[/red]")
                return
            
            response.raise_for_status()
            data = response.json()
            return data.get("tag_name", "").lstrip("v")
        
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            attempt += 1
            console.print(f"[yellow]Attempt {attempt}/{retries} failed: {e}[/yellow]")
            if attempt < retries:
                time.sleep(delay)
            else:
                console.print("[red]Maximum retry reached. Aborting[/red]")
                return

        except requests.exceptions.HTTPError as e:
            console.print(f"[red]HTTP error: {e}[/red]")
            return
        except (KeyError, ValueError):
            label = tag or "latest"
            console.print(f"[yellow]Unexpected response format for version '{label}'.[/yellow]")
            return

def download_file(url, dest_path, retries=3, delay=2):
    """Download from url to dest_path"""
    attempt = 0
    while attempt < retries:
        try:
            with requests.get(url, stream=True, timeout=(5, 60)) as response:
                response.raise_for_status()
                total_length = int(response.headers.get('content-length', 0))

                progress = Progress(
                    TextColumn("📥 [progress.description]{task.description}"),
                    BarColumn(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                )

                task_id = progress.add_task("Downloading", total=total_length)

                with progress, open(dest_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive chunks
                            file.write(chunk)
                            progress.update(task_id, advance=len(chunk))

            console.print(f"[green]File successfully downloaded to {dest_path}[/green]")
            return True

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            attempt += 1
            console.print(f"[yellow]Download attempt {attempt}/{retries} failed: {e}[/yellow]")
            if attempt < retries:
                time.sleep(delay)
            else:
                console.print("[red]Download failed after multiple attempts.[/red]")
                return False
        except requests.exceptions.HTTPError as e:
            console.print(f"[red]HTTP error: {e}[/red]")
            return False

def download_release_file(version, filename):
    """helper to download specific file based on the os

    Args:
        version (string): version
        filename (string): filename for specific os: geolistriksetup-{version}.exe or geolistrik-linux-{latest_version}.bin
    """
    url = f"https://github.com/{REPO}/releases/download/v{version}/{filename}"

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
    temp_file_path = temp_file.name
    temp_file.close()

    success = download_file(url, temp_file_path)

    if not success:
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                console.print(f"[cyan]Removed incomplete download: {temp_file_path}[/cyan]")
            except OSError as e:
                console.print(f"[yellow]Failed to remove temp file: {e}[/yellow]")
        return
    return temp_file_path

def update_windows(version):
    """CLI update on Windows"""
    filename = f"geolistriksetup-{version}.exe"
    installer_path = download_release_file(version, filename)
    if not installer_path:
        console.print("[red]Download failed. Aborting update.[/red]")
        return
        
    # Tentukan path exe lama
    install_dir = os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Geolistrik")
    exe_path = os.path.join(install_dir, "geolistrik.exe")
    
    # Backup exe lama (opsional)
    if os.path.exists(exe_path):
        backup_path = exe_path + ".bak"
        try:
            shutil.move(exe_path, backup_path)
            console.print(f"[cyan]Backup of old executable created: {backup_path}[/cyan]")
        except OSError as e:
            console.print(f"[yellow]Failed to backup old executable: {e}[/yellow]")

    console.print("[blue]Update downloaded successfully.[/blue]")
    console.print("[blue]Closing CLI and running installer...[/blue]")
    
    # Exit CLI agar installer bisa menimpa exe lama
    try:
        # Jalankan installer di proses baru sebelum exit
        subprocess.Popen(
            [installer_path],
            shell=False,  # tidak perlu shell=True
            close_fds=True
        )
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Failed to launch installer: {e}[/red]")
    finally:
        if os.path.exists(installer_path):
            try:
                os.remove(installer_path)
            except OSError:
                pass

def update_linux(version):
    """CLI update on Linux"""

    # make sure the script run with sudo
    if os.geteuid() != 0:
        console.print("[yellow]Run this command with sudo:[/yellow]")
        console.print("[yellow]sudo geolistrik update [--version or -v][/yellow]")
        sys.exit(1)

    filename = f"geolistrik-linux-{version}.bin"
    temp_file_path = download_release_file(version, filename)
    if not temp_file_path:
        console.print("[red]Download failed. Aborting update.[/red]")
        return

    dest_path = "/usr/local/bin/geolistrik"
    backup_path = f"{dest_path}.bak"

    # backup old binary if exists
    if os.path.exists(dest_path):
        try:
            shutil.copy2(dest_path, backup_path)
            console.print(f"[cyan]Backup of old binary created: {backup_path}[/cyan]")
        except OSError as e:
            console.print(f"[yellow]Failed to backup old binary: {e}[/yellow]")
    
    console.print(f"[blue]Updating {APP_NAME} in {dest_path} ...[/blue]")

    try:
        shutil.move(temp_file_path, dest_path)
        os.chmod(dest_path, 0o755)
    except OSError as e:
        console.print(f"[red]Failed to update {APP_NAME}: {e}[/red]")
        # restore backup if exists
        if os.path.exists(backup_path):
            shutil.move(backup_path, dest_path)
            console.print("[cyan]Restored old binary from backup.[/cyan]")
        return

    console.print(f"[green]Update successful! Now running geolistrik-cli v{version}.[/green]")

def update_cli(specific_version=None):
    """Check for update and show status"""
    console.print("[blue]Checking for updates...[/blue]")

    version = _fetch_github_release_tag(tag=specific_version)

    # faild to get version    
    if version is None:
        sys.exit(1)
        
    if version == CURRENT_VERSION:
        console.print(f"[green]Already up to date (v{CURRENT_VERSION})[/green]")
        return

    console.print(f"[yellow]Update available: v{version} (current: v{CURRENT_VERSION})[/yellow]")
    
    os_name = platform.system()
    updater = {"Windows": update_windows, "Linux": update_linux}.get(os_name)
    if updater:
        updater(version)
    else:
        console.print(f"[red]OS {os_name} not supported for auto-update.[/red]")
    