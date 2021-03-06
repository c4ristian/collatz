"""
This module provides methods to generate Collatz sequences and related features. All
functions are optimised for handling arbitrary big integers. The precision of
calculated float values depends on the precision of the underlying data type in
Python and pandas. The module provides functions for Collatz sequences both in the
original form *3v+1* as well as in the generalised variant *kv+c*.
"""

from collatz import commons as com


# pylint: disable=C0103
# A single character for k and c is ok
def generate_collatz_sequence(start_value, k=3, c=1, max_iterations=100):
    """
    This method generates a Collatz sequence for a specific start value,
    analyses its basic attributes and returns the result as a data frame.

    :param start_value: The start value as positive int.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :param max_iterations: The maximum number of iterations performed for the
        Collatz sequence (default is 100).
    :return: A pandas data frame with the results.
    """
    collatz_sequence = com.collatz_sequence(start_value, k, c, max_iterations)
    collatz_frame = com.analyse_collatz_basic_attributes(collatz_sequence)

    next_collatz = collatz_frame["collatz"].apply(com.next_collatz_number, args=(k, c,))
    next_odd = collatz_frame["collatz"].apply(com.next_odd_collatz_number, args=(k, c,))

    collatz_frame["collatz_index"] = collatz_frame.index
    collatz_frame["next_collatz"] = next_collatz
    collatz_frame["next_odd"] = next_odd
    collatz_frame.insert(1, "k_factor", [k] * len(collatz_frame))

    return collatz_frame


def generate_odd_collatz_sequence(start_value, k=3, c=1, max_iterations=100):
    """
    This method generates a Collatz sequence containing only odd numbers
    for a specific start value, analyses its basic attributes
    and returns the result as a data frame.

    :param start_value: The int value to start with. The value must be a
        natural number > 0. If an even number is handed over, the next odd number will be used
        as start value.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :param max_iterations: The maximum number of iterations performed for the
        Collatz sequence (default is 100).
    :return: A pandas data frame with the results.
    """
    collatz_sequence = com.odd_collatz_sequence(start_value, k, c, max_iterations)
    collatz_frame = com.analyse_collatz_basic_attributes(collatz_sequence)

    next_collatz = collatz_frame["collatz"].apply(com.next_collatz_number, args=(k, c,))
    next_odd = collatz_frame["collatz"].apply(com.next_odd_collatz_number, args=(k, c,))

    collatz_frame["odd_index"] = collatz_frame.index
    collatz_frame["next_collatz"] = next_collatz
    collatz_frame["next_odd"] = next_odd
    collatz_frame.insert(1, "k_factor", [k] * len(collatz_frame))

    return collatz_frame
