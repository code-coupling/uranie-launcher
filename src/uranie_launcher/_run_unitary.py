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
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument(
        "commands_json_file",
        help = "Name of the script or the command to execute")
    args = parser.parse_args(arguments)

    with open(args.commands_json_file, encoding = 'utf-8') as f:
        commands = json.load(f)

    for _command, _arguments in commands.items():
        try:
            proc = subprocess.run([_command] + _arguments,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                check = True)
            utils.info(f"{Path(__file__).name} : Start the execution of the command "
                       f"subprocess.run({[_command] + _arguments})")
            utils.info(f"{Path(__file__).name} : proc.stdout:")
            utils.info(proc.stdout.decode(encoding = 'utf-8'))
            utils.info(f"{Path(__file__).name} : proc.stderr:")
            utils.info(proc.stderr.decode(encoding = 'utf-8'))
            if proc.returncode == 0:
                utils.info(f"{Path(__file__).name} : The execution of the command "
                           f"subprocess.run({[_command] + _arguments}) was successful.")
            else:
                utils.info(f"{Path(__file__).name} : Failed to execute the command "
                           f"subprocess.run({[_command] + _arguments})\n"
                           f"{proc.stdout.decode(encoding = 'utf-8')} {proc.returncode}")
                return proc.returncode
        except subprocess.CalledProcessError:
            return 1

    return 0

def run_unitary():
    """ Entry point for the ``uranie-launcher-unitary`` script."""
    logging.getLogger(uranie_launcher_name).addHandler(logging.StreamHandler(sys.stdout))
    sys.exit(main_unitary(sys.argv[1:]))
