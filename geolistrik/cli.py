import os
import sys
import argparse
import threading

from geolistrik.commands import generate, update
from geolistrik.utils.update_cli import update_cli
from geolistrik.utils.check_update import check_update
from geolistrik.config import APP_NAME, VERSION, AUTHOR, CONTACT, WEBSITE, REPO

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

if sys.stdout.encoding.lower() != 'utf-8':
    console = Console(legacy_windows=True)
else:
    console = Console()

banner = f"""
███████╗████████╗ █████╗  ██████╗██╗  ██╗    ██╗████████╗██╗
██╔════╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ██║╚══██╔══╝██║
███████╗   ██║   ███████║██║     █████╔╝     ██║   ██║   ██║
╚════██║   ██║   ██╔══██║██║     ██╔═██╗     ██║   ██║   ╚═╝
███████║   ██║   ██║  ██║╚██████╗██║  ██╗    ██║   ██║   ██╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝   ╚═╝   ╚═╝
"""

def show_welcome():
    welcome_msg = Text()
    welcome_msg.append(banner, style="bold magenta")
    welcome_msg.append("\n\n")
    welcome_msg.append(f"⚡ Welcome to {APP_NAME}! v{VERSION}\n", style="bold green")
    welcome_msg.append("Geolistrik CLI is designed to assist geoelectrical surveyors\n", style="italic cyan")
    welcome_msg.append("in generating stacking charts and measurement tables quickly and easily.\n\n")

    welcome_msg.append("🔨 Usage:\n", style="bold yellow")
    welcome_msg.append("  geolistrik [code] [start] [end] [spacing] [--outdir folder]\n")
    welcome_msg.append("  for full options, use --help\n\n")

    welcome_msg.append("📚 Available configurations (code):\n", style="bold yellow")
    welcome_msg.append("  ws  - Wenner Schlumberger\n")
    welcome_msg.append("  wn  - Wenner\n")
    welcome_msg.append("  pp  - Pole Pole\n")
    welcome_msg.append("  pd  - Pole Dipole\n")
    welcome_msg.append("  dd  - Dipole Dipole\n\n")

    welcome_msg.append(f"🔗 Full documentation: {WEBSITE}")
    console.print(Panel(welcome_msg, title=f"[bold magenta]{APP_NAME}", expand=False))

def main():
    parser = argparse.ArgumentParser(
    prog="geolistrik",
    description="CLI tool for generating stacking charts and geoelectrical survey tables.",
    # epilog="Example: geolistrik ws 0 100 10 --outdir output/" # edit later
    )

    subparsers = parser.add_subparsers(dest="command")

    # register commands
    generate.register_subcommand(subparsers)

    # update commands
    update.register_subcommand(subparsers)

    def default_func(args):
        show_welcome()

        # run check_update() in the background
        t = threading.Thread(target=check_update, daemon=False)
        t.start()
        t.join(timeout=1)

    parser.set_defaults(func=default_func)

    args = parser.parse_args()
    args.func(args)