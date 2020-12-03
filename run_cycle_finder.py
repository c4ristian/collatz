"""
This script runs a program that tries to find cycles in Collatz
sequences and writes the results to disk.

Examples
--------
>>> python run_cycle_finder.py --k 201 --c 15 --v 1001 --f "data/cycles_c_15.csv"
"""

# Imports
import logging
import argparse
import shutil
from collatz.cycles import find_cycles


# Global variables
DATA_PATH = "data/"
DEFAULT_FILE_PATH = DATA_PATH + "cycles.csv"
DEFAULT_MAX_K = 999
DEFAULT_MAX_C = 1
DEFAULT_MAX_VALUE = 10000
DEFAULT_MAX_ITERATIONS = 100


def _parse_cmd_args():
    """
    This method parses the command line arguments of the program.
    :return: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='Run cycle finder.')
    parser.add_argument(
        "--k", help=("maximum k factor. Default is " + str(DEFAULT_MAX_K)),
        default=DEFAULT_MAX_K
    )

    parser.add_argument(
        "--c", help=("maximum c summand. Default is " + str(DEFAULT_MAX_C)),
        default=DEFAULT_MAX_C
    )

    parser.add_argument(
        "--v", help=("maximum odd start value. Default is "
                     + str(DEFAULT_MAX_VALUE)),
        default=DEFAULT_MAX_VALUE
    )

    parser.add_argument(
        "--f", help=("path of destination file. Default is '"
                     + str(DEFAULT_FILE_PATH) + "'"),
        default=DEFAULT_FILE_PATH
    )

    args = parser.parse_args()
    return args


def _main():
    """
    This method executes the program.
    :return: None.
    """
    # Configuration
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    # Parsing command line args
    args = _parse_cmd_args()
    logging.debug("Command line args: %s", args)

    k_factors = range(1, int(args.k) + 2, 2)
    max_c = int(args.c)
    max_value = int(args.v)
    export_file_name = args.f
    dest_file_name = export_file_name
    tmp_file_name = export_file_name + "_tmp"

    cycle_count = 0
    write_mode = True

    # Find cycles
    logging.info("Running cycle finder...")

    for k_factor in k_factors:
        logging.info("Finding cycles for k=%d", k_factor)

        cycle_frame = find_cycles(
            k_factor, max_c=max_c, max_value=max_value,
            max_iterations=DEFAULT_MAX_ITERATIONS)

        cycle_count = cycle_count + len(cycle_frame)

        # Write the frame to file
        mode_flag = "w" if write_mode else "a"
        cycle_frame.to_csv(
            tmp_file_name, mode=mode_flag, index=False, header=write_mode)
        write_mode = False

    # Moving tmp file to destination file
    logging.info("Moving temp file to destination file")
    shutil.move(tmp_file_name, dest_file_name)

    # Print results
    logging.info("%d cycle(s) found:", cycle_count)


# Main method to start the program
if __name__ == '__main__':
    _main()
