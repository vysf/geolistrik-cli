import os
import sys
import argparse
from geolistrik.config import APP_NAME, VERSION, AUTHOR, CONTACT, WEBSITE
from geolistrik.src import (
    wenner_schlumberger, wenner,
    pole_pole, pole_dipole, dipole_dipole
)

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

def show_welcom():
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
    epilog="Example: geolistrik ws 0 100 10 --outdir output/"
    )

    parser.add_argument("config", nargs="?", help="Configuration code: ws, wn, pp, pd, dd")
    parser.add_argument("start", nargs="?", type=float, help="Minimum electrode spacing")
    parser.add_argument("end", nargs="?", type=float, help="Maximum electrode spacing")
    parser.add_argument("spacing", nargs="?", type=float, help="Distance between electrodes")

    parser.add_argument("-v", "--version", action="store_true", help="Show application version")
    parser.add_argument("-V", action="store_true", help="Alias for --version")
    parser.add_argument("-about", action="store_true", help="Show application information")
    parser.add_argument(
        "--outdir", 
        default=".", 
        help="Output folder to save results (default: current folder)"
    )
    parser.add_argument(
        "--no-plot", 
        action="store_true", 
        help="Do not generate stacking chart image"
    )

    args = parser.parse_args()

    if args.version or args.V:
        print(f"{APP_NAME} v{VERSION}")
        return

    if args.about:
        print(f"{APP_NAME}\nVersion: {VERSION}\nAuthor: {AUTHOR}\nContact: {CONTACT}\nWebsite: {WEBSITE}")
        return

    if args.config is None:
        show_welcom()
        return

    config_map = {
        "ws": wenner_schlumberger.run,
        "wn": wenner.run,
        "pp": pole_pole.run,
        "pd": pole_dipole.run,
        "dd": dipole_dipole.run,
    }

    if args.config not in config_map:
        print("❌ Kode konfigurasi tidak valid. Gunakan: ws, wn, pp, pd, dd.")
        return

    if None in (args.start, args.end, args.spacing):
        print("❌ Argumen start, end, dan spacing wajib diisi.")
        return

    # Pastikan folder output ada
    os.makedirs(args.outdir, exist_ok=True)

    # Jalankan fungsi sesuai konfigurasi dan output folder
    config_map[args.config](args.start, args.end, args.spacing, output_dir=args.outdir, plot=not args.no_plot)
