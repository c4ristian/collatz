"""
This script runs a program that tries to find cycles in Collatz
sequences.
"""

# Imports
import logging
from collatz.cycles import find_cycles


def _main():
    """
    This method executes the program.
    :return: None.
    """
    # Configuration
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    k_factors = range(1, 1001, 2)
    cycle_lengths = range(1, 101)

    max_value = 10000

    # Try to find cycles
    logging.info("Running cycle finder...")

    cycles = {}
    cycle_count = 0

    for k_factor in k_factors:
        logging.info("Finding cycles for k=%d", k_factor)

        for length in cycle_lengths:
            next_cycles = find_cycles(
                k=k_factor, cycle_length=length, max_value=max_value)

            if next_cycles:
                if k_factor in cycles:
                    cycles[k_factor].append(next_cycles)
                else:
                    cycles[k_factor] = next_cycles
                cycle_count += len(next_cycles)

    # Print results
    logging.info("%d cycle(s) found:", cycle_count)
    logging.info(cycles)


# Main method to start the program
if __name__ == '__main__':
    _main()
