"""
This module provides methods to generate collatz sequences and related features.
"""

import random as rnd
import numpy as np
import pandas as pd
from collatz import commons as com


def generate_collatz_sequence(start_value, k=3, max_iterations=300):
    """
    This method generates a collatz sequence for a specific start value,
    analyses its basic attributes and returns the result as a data frame.

    :param start_value: The start value as positive integer.
    :param k: The factor that is multiplied with odd numbers (default is 3)
    :param max_iterations: The maximum number of iterations performed for the
    collatz sequence (default is 300).
    :return: A data frame with the results.
    """
    collatz_sequence = com.collatz_sequence(start_value, k, max_iterations)
    collatz_frame = com.analyse_collatz_basic_attributes(collatz_sequence)

    next_collatz = collatz_frame["collatz"].apply(com.next_collatz_number, args=(k,))
    next_odd = collatz_frame["collatz"].apply(com.next_odd_collatz_number, args=(k,))

    collatz_frame["collatz_index"] = collatz_frame.index
    collatz_frame["next_collatz"] = np.array(next_collatz, dtype=pd.Int64Dtype)
    collatz_frame["next_odd"] = np.array(next_odd, dtype=pd.Int64Dtype)
    collatz_frame.insert(1, "k_factor", k)

    return collatz_frame


def generate_random_sequence(max_start_value=50000, k_factors=3, max_iterations=300):
    """
    This method randomly generates a collatz sequence, analyses its numbers and returns
    the result as a data frame.

    :param max_start_value: The maximum starting value (default is 50000). Minimum start value is 1.
    :param k_factors: A list or tuple of factors that are multiplied with
    odd numbers (default is 3)
    :param max_iterations: The maximum number of iterations performed for a specific
    collatz sequence (default is 300).
    :return: A data frame with the results.
    """
    start_value = rnd.randint(1, max_start_value)
    k_factor = rnd.choice(k_factors)

    collatz_frame = generate_collatz_sequence(start_value, k_factor, max_iterations)
    return collatz_frame


# pylint: disable=C0103
# A single character for n is ok
def generate_random_sequences(n, max_start_value=50000, k_factors=3, max_iterations=300):
    """
    This method randomly generates n collatz sequences, analyses their numbers
    and returns the results as a data frame.

    :param n: The number of collatz sequences to generate.
    :param k_factors: A list or tuple of factors that are multiplied with odd numbers (default is 3)
    :param max_start_value: The maximum starting value (default is 50000). Minimum start value is 1.
    :param max_iterations: The maximum number of iterations performed for
    specific a collatz sequence (default is 300).
    :return: None.
    """
    # Create sequences
    output_frame = None

    for i in range(0, n):
        new_collatz_frame = generate_random_sequence(max_start_value, k_factors, max_iterations)
        new_collatz_frame.insert(0, "sequence_index", i)

        if output_frame is None:
            output_frame = new_collatz_frame
        else:
            output_frame = output_frame.append(new_collatz_frame)

    # Return results
    return output_frame
