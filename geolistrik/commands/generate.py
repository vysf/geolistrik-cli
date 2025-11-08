import os
import sys
import argparse
from geolistrik.src import (
    wenner_schlumberger, wenner,
    pole_pole, pole_dipole, dipole_dipole
)

# test scenario
# unit test
# 1. cek apa yang terjadi jika command `generate` tanpa start_position, end_position dan spacing
# 2. cek tipe data tanpa start_position, end_position dan spacing jika tidak sesuai
# 3. Cek validasi start_position < end_position
# 4. Pastikan error muncul saat start_position >= end_position.
# 5. Cek validasi spacing positif
# 6. Pastikan error muncul saat spacing <= 0.
# 7. Cek flag --no-plot dan --verbose
# 8. Pastikan flag no_plot dan verbose mengatur parameter yang tepat di fungsi.
# 9. Cek nilai default outdir
# 10. Pastikan kalau --outdir tidak disediakan, nilai default "." digunakan.

# integration test
# 1. config_map menjalankan fungsinya dengan baik
# 2. Cek output file/folder
# 3. Setelah generate dijalankan, cek apakah file output (chart, excel, dll) dihasilkan di folder yang benar.
# 4. Cek fungsi-fungsi run di config_map menerima argumen yang benar
# 5. Mock fungsi-fungsi di config_map lalu cek apakah mereka dipanggil dengan argumen yang sesuai.
# 6. Cek behaviour ketika flag --no-plot aktif
# 7. Pastikan fungsi generate tidak membuat gambar chart ketika no_plot aktif.

def register_subcommand(subparsers):
    generate_parser = subparsers.add_parser(
        "generate",
        help='Generate stacking chart and excel file',
        description='Generate stacking chart and excel file for geolistrik survey.'
    )

    generate_parser.add_argument(
        "--configuration", 
        "-c", 
        required=True,
        choices=["wn", "ws", "pp", "dd", "pd"], 
        help="Configuration code: ws, wn, pp, pd, dd"
    )
    generate_parser.add_argument(
        "--start-position", 
        "-s", 
        type=float,
        required=True,
        help="Start electrode position in meter"
    )
    generate_parser.add_argument(
        "--end-position", 
        "-e", 
        type=float,
        required=True,
        help="End electrode position in meter"
    )
    generate_parser.add_argument(
        "--spacing", 
        "-a", 
        type=float,
        required=True,
        help="Minimun distance between electrode spacing"
    )
    generate_parser.add_argument(
        "--outdir",
        "-o", 
        default=".", 
        help="Output folder to save results (default: current folder)"
    )
    generate_parser.add_argument(
        "--no-plot",
        action="store_true", 
        help="Do not generate stacking chart image"
    )
    generate_parser.add_argument(
        "--verbose",
        action="store_true", 
        help="Enable verbose output for debugging"
    )

    generate_parser.set_defaults(func=handle_generate)

def handle_generate(args):
    if args.start_position >= args.end_position:
        print("Start position must be less than end position.")
        sys.exit(1)

    config_map = {
        "ws": wenner_schlumberger.run,
        "wn": wenner.run,
        "pp": pole_pole.run,
        "pd": pole_dipole.run,
        "dd": dipole_dipole.run,
    }

    os.makedirs(args.outdir, exist_ok=True)

    config_map[args.configuration](
        args.start_position,
        args.end_position,
        args.spacing, 
        output_dir=args.outdir,
        plot=not args.no_plot,
        verbose=args.verbose
    )
