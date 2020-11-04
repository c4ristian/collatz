"""
This module provides methods to create and analyse Collatz graphs. All
functions are optimised for handling arbitrary big integers. The precision of
calculated float values depends on the precision of the underlying data type in
Python and pandas.
"""

import pandas as pd
import sympy
from collatz import commons


def get_odd_predecessor(odd_int, index, k=3):
    """
    This method calculates the odd predecessor for a certain odd number in a Collatz graph.
    For every odd number there are n predecessors. The variable index [0..n] specifies which
    predecessor is returned. The method is based on a deterministic algorithm.
    It currently works only for the k-factors (1,3,5,7,9).

    :param odd_int: The node for which the predecessor is calculated.
    :param index: The index of the predecessor as int [0..n].
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :return: The predecessor or None if no predecessor exists.
    """
    # Validate input parameters
    assert odd_int > 0, "Value > 0 expected"

    mod_result = odd_int % 2
    assert mod_result == 1, "Not an odd number"

    # Return None if no predecessors exist
    if k > 1 and odd_int % k == 0:
        return None

    result = None

    if k == 1:
        result = (odd_int * 2 ** ((k - odd_int % k) + index) - 1) // k
    elif k == 3:
        result = (odd_int * 2 ** ((k - odd_int % k) + (2 * index)) - 1) // k
    elif k == 5:
        power_dict = {0: None, 3: 1, 4: 2, 2: 3, 1: 4}
        power = power_dict[odd_int % 5]
        if power:
            result = (odd_int * 2 ** (power + (4 * index)) - 1) // k
    elif k == 7:
        power_dict = {0: None, 1: 3, 2: 2, 3: None, 4: 1, 5: None, 6: None}
        power = power_dict[odd_int % 7]
        if power:
            result = (odd_int * 2 ** (power + (3 * index)) - 1) // k
    elif k == 9:
        power_dict = {0: None, 1: 6, 2: 5, 3: None, 4: 4, 5: 1, 6: None, 7: 2, 8: 3}
        power = power_dict[odd_int % 9]
        if power:
            result = (odd_int * 2 ** (power + (6 * index)) - 1) // k
    else:
        raise TypeError("Parameter k not in (1,3,5,7,9)")

    return result


def get_odd_predecessor_generalised(odd_int, index, k=3, max_iterations=1000):
    """
    This method calculates the odd predecessor for a certain odd number in a Collatz graph.
    For every odd number there are n predecessors. The variable index [0..n] specifies which
    predecessor is returned. The method is based on a generalised algorithm that builds on
    the multiplicative order of the given k factor and a discrete logarithm.
    If a predecessor cannot be determined for the k factor None is returned.

    :param odd_int: The node for which the predecessor is calculated.
    :param index: The index of the predecessor as int [0..n].
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param max_iterations: The maximum number of iterations used to
        determine the multiplicative order (default is 1000).
    :return: The predecessor or None if no predecessor exists.
    """
    # Validate input parameters
    assert odd_int > 0, "Value > 0 expected"

    mod_result = odd_int % 2
    assert mod_result == 1, "Not an odd number"

    # Return None if no predecessors exist
    if k > 1 and odd_int % k == 0:
        return None

    result = None
    order = commons.multiplicative_order(k, max_iterations=max_iterations)

    if order is not None:
        try:
            dlog = sympy.discrete_log(k, odd_int, 2)
        except ValueError:
            dlog = None

        if dlog is not None:
            result = (odd_int * 2**(order * index + order - dlog) - 1) // k

    return result


def get_right_sibling(odd_int: int, index: int, k=3, max_iterations=1000):
    """
    This method calculates the right sibling for a certain odd number in a Collatz graph.
    For every odd number there are n right siblings. The variable index [0..n] specifies which
    sibling is returned. The method is based on a deterministic algorithm that builds on
    the multiplicative order of the given k factor. If a sibling cannot be
    determined for the k factor None is returned.

    :param odd_int: The node for which the right sibling is calculated.
    :param index: The index of the sibling as int [0..n].
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param max_iterations: The maximum number of iterations used to
        determine the multiplicative order (default is 1000).
    :return: The right sibling or None, if no sibling can be determined for the k factor.
    """
    # Validate input parameters
    assert odd_int > 0, "Value > 0 expected"

    mod_result = odd_int % 2
    assert mod_result == 1, "Not an odd number"

    sibling = None
    order = commons.multiplicative_order(k, max_iterations=max_iterations)

    if order is not None:
        index_p = index + 1
        sibling = odd_int * 2**(index_p * order)
        sibling = sibling + ((2**order - 1) // k) * ((2**(index_p * order) - 1) // (2**order - 1))

    return sibling


def create_collatz_graph(start_value, k=3, predecessor_count=3, iteration_count=3):
    """
    This method creates a Collatz graph consisting of odd numbers, starting with a
    certain odd integer as root node. The method determines the predecessors
    of the root node using the function get_odd_predecessor.

    :param start_value: Odd integer as root node.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param predecessor_count: The number of predecessors to determine for every node.
    :param iteration_count: The number of iterations to perform. This parameter determines
        the depth of the tree.
    :return: The Collatz graph as data frame.
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


def get_odd_binary_predecessors(odd_int: int):
    """
    This method returns the predecessors of a node in a binary Collatz graph
    as described in the paper
    *Pruning the binary tree, proving the Collatz conjecture* (https://arxiv.org/abs/2008.13643).
    The method internally builds on the function get_odd_predecessor. It is implemented for
    the k-factor 3 exclusively.

    :param odd_int: The node for which the predecessors are calculated.
    :return: The predecessors or an empty list if the odd int is a multiple of 3.
    """
    predecessors = []

    first_child = get_odd_predecessor(odd_int, k=3, index=0)

    if first_child is not None and first_child % 3 == 0:
        first_child = get_odd_predecessor(odd_int, k=3, index=1)

    if first_child is not None:
        first_sibling = odd_int * 4 + 1
        if first_sibling % 3 == 0:
            first_sibling = first_sibling * 4 + 1

        predecessors.append(first_sibling)
        predecessors.append(first_child)

    return predecessors


def create_dutch_graph(start_value, iteration_count=3):
    """
    This function creates the binary Collatz graph *T>=0* as described in the paper
    *Pruning the binary tree, proving the Collatz conjecture* (https://arxiv.org/abs/2008.13643).
    The method internally builds on the function get_odd_binary_predecessors. It is
    implemented for the k-factor 3 exclusively.

    :param start_value: Odd integer as root node.
    :param iteration_count: The number of iterations to perform. This parameter determines
        the depth of the tree.
    :return: The Collatz binary graph as data frame.
    """
    # Return empty frame if node is leaf
    if start_value % 3 == 0:
        return pd.DataFrame({
            "iteration": [],
            "successor": [],
            "predecessor": []
        })

    # Create graph
    iterations = []
    successors = []
    predecessors = []

    current_successors = [start_value]

    for i in range(1, iteration_count + 1):
        next_successors = []

        for successor in current_successors:
            current_predecessors = get_odd_binary_predecessors(successor)
            iterations.extend([i, i])
            successors.extend([successor, successor])
            predecessors.extend(current_predecessors)
            next_successors.extend(current_predecessors)

        current_successors = next_successors

    dutch_frame = pd.DataFrame({
        "iteration": pd.Series(iterations),
        "successor": pd.Series(successors, dtype="object"),
        "predecessor": pd.Series(predecessors, dtype="object")
    })

    # Drop duplicate values
    dutch_frame = dutch_frame.drop_duplicates(
        subset=["successor", "predecessor"]).reset_index(drop=True)

    return dutch_frame


def get_pruned_binary_predecessors(odd_int: int, pruning_level=0):
    """
    This method returns the pruned predecessors of a node in a binary Collatz graph
    as described in the paper
    *Pruning the binary tree, proving the Collatz conjecture* (https://arxiv.org/abs/2008.13643).
    The method internally builds on the function get_odd_binary_predecessors. The method is
    implemented for the k-factor 3 exclusively. In case of an illegal starting node
    an AssertionError is thrown.

    :param odd_int: The node for which the predecessors are calculated.
    :param pruning_level: The pruning level p. The default value p=0 leads to an unpruned tree.
    :return: The predecessors as list.
    """
    assert odd_int % 3 > 0

    binary_predecessors = get_odd_binary_predecessors(odd_int)
    pruned_predecessors = []

    if binary_predecessors:
        left_pred = binary_predecessors[0]
        right_pred = binary_predecessors[1]

        if pruning_level > 0:
            right_anc = odd_int

            for _ in range(0, pruning_level):
                right_anc = (right_anc - 1) // 4
                if right_anc % 3 == 0:
                    right_anc = (right_anc - 1) // 4

            right_pred = get_odd_binary_predecessors(right_anc)[1]

            for _ in range(0, pruning_level):
                right_pred = get_odd_binary_predecessors(right_pred)[0]

        pruned_predecessors.append(left_pred)
        pruned_predecessors.append(right_pred)

    return pruned_predecessors


def create_pruned_dutch_graph(pruning_level=0, iteration_count=3):
    """
    This function creates a pruned binary Collatz graph *T>=p* as described in the paper
    *Pruning the binary tree, proving the Collatz conjecture* (https://arxiv.org/abs/2008.13643).
    The method internally builds on the function get_pruned_binary_predecessors. It is
    implemented for the k-factor 3 exclusively.

    :param pruning_level: The pruning level p. The default value p=0 leads to an unpruned tree.
    :param iteration_count: The number of iterations to perform. This parameter determines
        the depth of the tree.
    :return: The pruned Collatz binary graph as data frame.
    """
    # Determine starting node
    starting_node = 1

    for i in range(0, pruning_level):
        starting_node = starting_node * 4 + 1

        if starting_node % 3 == 0:
            starting_node = starting_node * 4 + 1

    # Determine first predecessor
    first_pred = starting_node * 4 + 1

    if first_pred % 3 == 0:
        first_pred = first_pred * 4 + 1

    # Create graph
    iterations = [1, 1]
    successors = [starting_node, starting_node]
    predecessors = [first_pred, starting_node]

    current_successors = [first_pred]

    for i in range(1, iteration_count + 1):
        next_successors = []

        for successor in current_successors:
            current_predecessors = get_pruned_binary_predecessors(
                successor, pruning_level=pruning_level)

            iterations.extend([i, i])
            successors.extend([successor, successor])
            predecessors.extend(current_predecessors)
            next_successors.extend(current_predecessors)

        current_successors = next_successors

    dutch_frame = pd.DataFrame({
        "iteration": pd.Series(iterations),
        "successor": pd.Series(successors, dtype="object"),
        "predecessor": pd.Series(predecessors, dtype="object")
    })

    return dutch_frame
