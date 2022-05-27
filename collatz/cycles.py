"""
This module provides methods to analyse cycles in Collatz sequences. It
covers Collatz sequences both in the original form *3v+1* as well as in
the generalised variant *kv+c*.
"""

# Imports
from math import log2
import pandas as pd
from collatz import commons


# pylint: disable=C0103
# A single character for k and c is ok
def find_cycles(k: int, max_c: int, max_value=1000, max_iterations=100):
    """
    This method finds cycles in Collatz sequences for a specific k factor
    and certain ranges of the summand c and the first odd number of a
    sequence. Each cycle is counted only once, starting with the lowest
    odd number. For *k=5* and *c=1* are, for example, only the cycles
    (1,3), (13, 33, 83) and (17, 43, 27) returned.

    :param k: The factor by which odd numbers are multiplied in the sequence.
    :param max_c: The maximum summand c to consider. The cycles are searched
        in the range (1,max_c + 2, 2).
    :param max_value: The highest odd number to be considered in the search. The odd
        starting numbers are searched in the range (1, max_value + 2, 2). Default is 1000.
    :param max_iterations: The maximum number of iterations performed
        within a sequence before the method exits. Default is 100.
    :return: A pandas data frame with the identified cycles.
    """
    result_frame = find_cycles_in_ranges(
        k=range(k, k + 2, 2), c=range(1, max_c + 2, 2),
        max_value=max_value, max_iterations=max_iterations)

    return result_frame


def find_cycles_in_ranges(k: range, c: range, max_value=1000, max_iterations=100):
    """
    This method finds cycles in Collatz sequences for certain ranges of k, c and
    odd starting values. Each cycle is counted only once, starting with the lowest
    odd number. For *k=5* and *c=1* are, for example, only the cycles
    (1,3), (13, 33, 83) and (17, 43, 27) returned.

    :param k: The range of the factors by which odd numbers are multiplied in the sequence.
    :param c: The range of the summands by which odd numbers in the sequence are increased.
    :param max_value: The highest odd number to be considered in the search. The odd
        starting numbers are searched in the range (1, max_value + 1, 2). Default is 1000.
    :param max_iterations: The maximum number of iterations performed
        within a sequence before the method exits. Default is 100.
    :return: A pandas data frame with the identified cycles.
    """
    result_frame = pd.DataFrame({
        "k": [],
        "c": [],
        "length": [],
        "v_1": [],
        "values": []}, dtype='object'
    )

    for current_k in k:
        for current_c in c:
            odd_set = set()

            for start_value in range(1, max_value + 1, 2):
                odds = commons.odd_collatz_sequence(
                    start_value=start_value, k=current_k, c=current_c,
                    max_iterations=max_iterations)

                cycle_found = odds[0] == odds[-1]
                cycle_found &= odds[0] not in odd_set

                if cycle_found:
                    cycle_frame = pd.DataFrame({
                        "k": [current_k],
                        "c": [current_c],
                        "length": [len(odds)-1],
                        "v_1": start_value,
                        "values": ",".join(map(str, odds[0:-1]))
                    })

                    odd_set.update(odds)

                    result_frame = pd.concat(
                        [result_frame, cycle_frame], ignore_index=True)

    result_frame = result_frame.reset_index(drop=True)
    return result_frame


def predict_cycle_alpha(k: int, cycle_length: int):
    """
    This method calculates the alpha (exponent of the power of 2) for a
    hypothetical cycle with a certain length for a Collatz sequence
    with a specific k factor.

    The method uses a formula that is based on the function math.log2. The
    returned value may be inaccurate for very big input values, due to the
    limitations of Python.

    :param k: The k factor as int.
    :param cycle_length: The number of odd numbers that are part of the cycle.
    :return: The alpha as int.
    """
    assert k > 0, "k factor must be > 0"
    assert cycle_length > 0, "cycle length must be > 0"

    alpha = int(log2(k) * cycle_length) + 1
    return alpha
