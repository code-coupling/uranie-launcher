""" Script to emulate the unitary calculation program.
"""

# ma fonction qui remplace ib-run, uranie-post-process, ...
import argparse
import json
import random
import sys
from pathlib import Path


def _read_input_file(input_filename):
    input_absolute_filename = Path(__file__).absolute().parent / input_filename
    with open(input_absolute_filename, 'r', encoding = 'utf-8') as input_file:
        return json.load(input_file)


def _do_calculation(uncertain_variable):
    # approximate the value of Pi
    n = uncertain_variable
    inside_circle = 0

    for i in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x ** 2 + y ** 2 <= 1:
            inside_circle += 1

    pi = 4 * inside_circle / n
    return pi


def _write_result(result, output_filename):
    output_absolute_filename = Path(__file__).absolute().parent / output_filename
    Path.mkdir(output_absolute_filename.parent, exist_ok=True)
    with open(output_absolute_filename, 'w', encoding = 'utf-8') as output_file:
        json.dump(result, output_file)


def main_unitary_calculation(arguments):
    # Interpret arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "data_filename",
        help="Name of the input data file describing the transient scenario "
             "(COMM or XML)")
    parser.add_argument(
        "output_dirname",
        help="Name of the directory where to store the results of the transient")
    args = parser.parse_args(arguments)

    data = _read_input_file(args.data_filename)
    uncertain_variable = data["uncertain_variable"]

    result = _do_calculation(uncertain_variable)

    output_dirname = Path(__file__).absolute().parent / args.output_dirname
    output_filename = output_dirname / "result"
    _write_result(result, output_filename)

    return 0


if __name__ == "__main__":
    sys.exit(main_unitary_calculation(sys.argv[1:]))
