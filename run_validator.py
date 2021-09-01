"""
This script uses tensorflow to validate a batch of Collatz numbers. The validation
checks if the numbers end with one as expected by Lothar Collatz.

In order to run the script in an acceptable amount of time a GPU is required. Due to
limitations of tensorflow no arbitrary big integers are supported.
"""

# Imports
import logging
import tensorflow as tf
from collatz import tensor as tc


# Global variables
START_NUMBER = 1
MAX_NUMBER = 2**25


def _main():
    # Setup
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info("Num GPUs available %s", len(tf.config.list_physical_devices('GPU')))

    # Perform validation
    odds_rng = range(START_NUMBER, MAX_NUMBER + 1)
    odds = tf.constant(odds_rng, dtype=tf.int64)

    logging.info(
        "Validating %d Collatz sequences", len(odds))

    counter = 0

    while tf.reduce_sum(odds) > tf.size(odds):
        # Filter ones
        ones = tf.not_equal(odds, 1)
        odds = tf.boolean_mask(odds, ones)

        # Calculate predecessors
        evens = tc.next_even_collatz_numbers(odds)
        odds = tc.next_odd_collatz_numbers(evens)
        counter = counter + 1

    logging.info("Validation successful!")
    logging.info("Max length: %d", counter)


# Main block to start the program
if __name__ == '__main__':
    _main()
