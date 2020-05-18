"""
This module contains methods to create and analyse collatz graphs.
"""

from math import log2
import warnings
import pandas as pd


def get_odd_predecessor(odd_int, index, k=3):
    """
    This method calculates the odd predecessor for a certain odd number in a collatz graph.
    For every odd number there are n predecessors. The variable index [0..n] specifies which
    predecessor is returned. The method is based on a deterministic algorithm.
    It currently works only for the k-factors (1,3,5).

    The function is optimised for handling arbitrary big integers.

    :param odd_int: The odd number the predecessor is calculated for.
    :param k: The factor odd numbers are multiplied with.
    :param index: The index of the predecessor as integer [0..n].
    :return: The predecessor or None if no predecessor exists.
    """
    # Validate input parameters
    assert odd_int > 0, "Value > 0 expected"

    mod_result = odd_int % 2
    assert mod_result == 1, "Not an odd number"

    # Return None if no predecessors exist
    if k > 1 and odd_int % k == 0:
        return None

    factor = 2 ** int(log2(k))

    if k == 1:
        result = (odd_int * 2 ** ((k - odd_int % k) + factor * index) - 1) // k
    elif k == 3:
        result = (odd_int * 2 ** ((k - odd_int % k) + (factor * index)) - 1) // k
    elif k == 5:
        power_dict = {0: 0, 3: 1, 4: 2, 2: 3, 1: 4}
        power = power_dict[odd_int % 5]
        result = (odd_int * 2 ** (power + (factor * index)) - 1) / k
    else:
        raise TypeError("Parameter k not in (1,3,5)")

    if result % 1 != 0:
        result = None

    return result


def get_odd_predecessors(collatz_int, k=3, power_range=range(1, 21)):
    """
    This method returns the odd predecessors of a number in
    a collatz graph. The predecessors are determined by an iterative process. This process
    uses powers of 2 to calculate the results.

    The function is limited to the pandas data type int64. It tries to detect
    overflows when the numbers get too big. In this case a warning is issued.

    :param collatz_int: The collatz number the predecessors are calculated for.
    :param k: The factor the odd numbers are multiplied with in the collatz sequence
    (default 3).
    :param power_range: The range of powers of two that is used for the calculation
    (default is (range(1, 21)).
    :return: A list of predecessors and the corresponding powers.
    """
    # Validate input parameters
    assert collatz_int > 0, "Value > 0 expected"

    mod_result = collatz_int % 2
    assert mod_result in (0, 1), "Not a whole number"

    power_array = pd.Series(power_range)
    predecessors = (collatz_int * 2 ** power_array - 1) / k

    # Try to detect a possible overflow
    odd = predecessors % 2 == 1
    even = predecessors % 2 == 0

    if sum(even) > 0:
        warnings.warn("Results filtered due to possible overflow")

    # Return predecessors
    whole_numbers = predecessors.apply(float.is_integer)

    predecessors = predecessors[whole_numbers & odd]
    powers = power_array[whole_numbers & odd]

    return list(predecessors.astype('int64')), list(powers)


def create_collatz_graph(start_value, k=3, predecessor_count=3, iteration_count=3):
    """
    This method creates an inverse collatz graph, consisting of odd numbers, beginning with a
    certain odd starting integer value. It currently works only for the k-factors (1,3,5).

    The function is optimised for handling big integers.

    :param start_value: Odd integer to start the graph with.
    :param k: The factor odd numbers are multiplied with in the sequence (default 3).
    :param iteration_count: The number of iterations to perform. This parameter determines
    the depth of the tree.
    :param predecessor_count: The number of predecessors to determine for every odd number.
    :return: The collatz graph as data frame.
    """
    result_frame = pd.DataFrame({
        "iteration": [],
        "successor": [],
        "predecessor": []
    }, dtype='object')

    successors = [start_value]

    for i in range(0, iteration_count):
        for suc in successors:
            predecessors = []

            for pred in range(0, predecessor_count):
                predecessors.append(get_odd_predecessor(suc, pred, k=k))

            new_frame = pd.DataFrame({
                "iteration": i+1,
                "successor": suc,
                "predecessor": predecessors
            }, dtype='object')

            result_frame = result_frame.append(new_frame).dropna()

        successors = result_frame[result_frame["iteration"] == i+1]["predecessor"]

    result_frame = result_frame.drop_duplicates(
        subset=["successor", "predecessor"]).reset_index(drop=True)

    return result_frame
