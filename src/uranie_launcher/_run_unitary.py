""" Script to launch Uranie from the bench.
"""

import json
import logging
import subprocess
import sys
import argparse
from pathlib import Path
from uranie_launcher import __name__ as uranie_launcher_name
from uranie_launcher import utils


def main_unitary(arguments):
    """ Run the unitary function with the given command line arguments.

    Parameters
    ----------
    arguments: list of str
        Command line arguments.

    Returns
    -------
    int
        Return code.
    """
    # Interpret arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "commands_json_file",
        help="Name of the script or the command to execute")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="activate debug mode (default: %(default)s)")
    args = parser.parse_args(arguments)

    utils.set_verbosity(utils.DEBUG if args.debug else utils.INFO)

    with open(args.commands_json_file, encoding='utf-8') as f:
        commands = json.load(f)

    for _command, _arguments in commands.items():
        utils.info(f"{Path(__file__).name} : Start the execution of the command "
                   f"subprocess.run({[_command] + _arguments})")
        proc = subprocess.run([_command] + _arguments,  # pylint: disable=subprocess-run-check
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

        utils.info(f"{_command} : proc.stdout:")
        utils.info(proc.stdout.decode(encoding='utf-8'))
        utils.info(f"{_command} : proc.stderr:")
        utils.info(proc.stderr.decode(encoding='utf-8'))
        if proc.returncode == 0:
            utils.info(f"The execution of the command "
                       f"subprocess.run({[_command] + _arguments}) was successful.")
        else:
            utils.info(f"Failed to execute the command "
                       f"subprocess.run({[_command] + _arguments}). Returned {proc.returncode}.")
            return proc.returncode

    return 0


def run_unitary():
    """ Entry point for the ``uranie-launcher-unitary`` script."""
    logging.getLogger(uranie_launcher_name).addHandler(logging.StreamHandler(sys.stdout))
    sys.exit(main_unitary(sys.argv[1:]))
