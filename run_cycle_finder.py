"""
This script runs a program that tries to find cycles in Collatz
sequences.
"""

# Imports
import logging
from collatz.cycles import find_cycles


# Main method to start the program
if __name__ == '__main__':

    # Configuration
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    # K_FACTORS = range(1, 1001, 2)
    # CYCLE_LENGTHS = range(1, 101)
    K_FACTORS = range(1, 5)
    CYCLE_LENGTHS = range(1, 3)

    MAX_VALUE = 10000

    # Try to find cycles
    CYCLES = {}
    CYCLE_COUNT = 0

    for k_factor in K_FACTORS:
        for length in CYCLE_LENGTHS:
            next_cycles = find_cycles(
                k=k_factor, cycle_length=length, max_value=MAX_VALUE)

            if next_cycles:
                if k_factor in CYCLES:
                    CYCLES[k_factor].append(next_cycles)
                else:
                    CYCLES[k_factor] = next_cycles
                CYCLE_COUNT += len(next_cycles)

    # Print results
    logging.info("%d cycle(s) found:", CYCLE_COUNT)
    logging.info(CYCLES)
