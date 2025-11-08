# 1. register command update: it will update with latest version
# 2. optional --version or argument version to choose current version

import sys
from geolistrik.utils.update_cli import update_cli

def register_subcommand(subparsers):
  update_parser = subparsers.add_parser(
      "update",
      help='Update cli to the latest version or current version ([version number] or --version [version number])',
      description='Update cli.'
  )

  update_parser.add_argument(
    "--version",
    "-v",
    required=False,
    help="Option for specific version"
  )

  update_parser.set_defaults(func=handle_update)

def handle_update(args):
  target_version = args.version
  update_cli(specific_version=target_version)
  sys.exit(0)
  return