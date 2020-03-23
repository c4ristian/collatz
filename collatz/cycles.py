"""
This module contains methods to analyse cycles in collatz sequences.
"""

# Imports
from math import log2
from collatz import commons


def find_cycles(k: int, cycle_length: int, max_value: int):
    """
    This method tries to find cycles in a collatz sequences for a
    specific k factor and a specific cycle-length. The cycle
    length is determined by the amount of odd numbers that
    are part of the cycle. The parameter max_value determines the
    highest odd number to be considered in the search.
    :param k: The k factor.
    :param cycle_length: The expected cycle length.
    :param max_value: The highest odd number to be considered
    in the search.
    :return: A list with cycles and their odd numbers of an empty list,
    if no cycles were found.
    """

    # Find cycles
    cycles = []
    odd_set = set()

    for i in range(1, max_value + 1, 2):
        odds = [None] * (cycle_length + 1)
        odds[0] = i
        current_odd = i

        for c in range(1, cycle_length + 1):
            current_odd = commons.next_odd_collatz_number(current_odd, k=k)
            odds[c] = current_odd

        cycle_found = odds[0] == odds[cycle_length]
        cycle_found &= len(set(odds)) >= cycle_length
        cycle_found &= odds[0] not in odd_set

        if cycle_found:
            cycles.append(odds)
            odd_set.update(odds)

    return cycles


def calculate_cycle_alpha(k: int, cycle_length: int, algorithm="simple"):
    """
    This method calculates the alpha (exponent of the power of 2) for a
    hypothetical cycle with a certain length for a collatz sequence
    with a specific k factor. The method uses an experimental formula
    to calculate the result.
    :param k: The k factor as int.
    :param cycle_length: The number of odd numbers that
    are part of the cycle.
    :param algorithm: Either "simple" or "lambda".
    :return: The alpha as int.
    """
    assert k > 0, "k factor must be > 0"
    assert cycle_length > 0, "cycle length must be > 0"
    assert algorithm in {"simple", "lambda", "max"}

    if algorithm == "simple":
        alpha = _calculate_alpha_simple(k, cycle_length)
    elif algorithm == "lambda":
        alpha = _calculate_alpha_lambda(k, cycle_length)
    elif algorithm == "max":
        alpha = _calculate_alpha_max(k, cycle_length)

    return alpha


def _calculate_alpha_simple(k: int, cycle_length: int):
    return int(log2(k)) * cycle_length + 1


def _calculate_alpha_lambda(k: int, cycle_length: int):
    simple = _calculate_alpha_simple(k, cycle_length)
    _lambda = int(cycle_length * (log2(k) - int(log2(k))) - 1)
    return simple + max(0, _lambda)


def _calculate_alpha_max(k: int, cycle_length: int):
    alpha = int(log2(k) * cycle_length) + 1
    return alpha
