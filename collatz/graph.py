"""
This module provides methods to create and analyse Collatz graphs.
"""

import pandas as pd


def get_odd_predecessor(odd_int, index, k=3):
    """
    This method calculates the odd predecessor for a certain odd number in a Collatz graph.
    For every odd number there are n predecessors. The variable index [0..n] specifies which
    predecessor is returned. The method is based on a deterministic algorithm.
    It currently works only for the k-factors (1,3,5,7,9).

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


def create_collatz_graph(start_value, k=3, predecessor_count=3, iteration_count=3):
    """
    This method creates a Collatz graph consisting of odd numbers, starting with a
    certain odd integer as root node. The method determines the predecessors
    of the root node using the function get_odd_predecessor.

    The function is optimised for handling arbitrary big integers.

    :param start_value: Odd integer as root node.
    :param k: The factor odd numbers are multiplied with in the sequence (default 3).
    :param predecessor_count: The number of predecessors to determine for every node.
    :param iteration_count: The number of iterations to perform. This parameter determines
    the depth of the tree.
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


def create_reverse_graph(start_value, k=3, successor_count=3, iteration_count=3):
    """
    This method creates a reverse Collatz graph consisting of odd numbers, starting with a
    certain odd integer as root node. The method internally builds on the function
    create_collatz_graph and swaps the successor and predecessor columns.

    The function is optimised for handling arbitrary big integers.

    :param start_value: Odd integer as root node.
    :param k: The factor odd numbers are multiplied with in the sequence (default 3).
    :param successor_count: The number of successors to determine for every node.
    :param iteration_count: The number of iterations to perform. This parameter determines
    the depth of the tree.
    :return: The collatz graph as data frame.
    """
    graph_frame = create_collatz_graph(start_value, k, successor_count, iteration_count)
    predecessor = list(graph_frame["predecessor"])
    successor = list(graph_frame["successor"])

    graph_frame["predecessor"] = successor
    graph_frame["successor"] = predecessor
    return graph_frame


def create_dutch_graph(start_value, successor_count=3, iteration_count=3):
    """
    This function creates a reverse binary Collatz graph as described in the paper
    [Pruning the binary tree, proving the Collatz conjecture](https://arxiv.org/abs/2008.13643).
    The method internally builds on the function create_reverse_graph. The method is
    implemented for the k-factor 3 exclusively.

    :param start_value: Odd integer as root node.
    :param successor_count: The number of successors to determine for every node.
    :param iteration_count: The number of iterations to perform. This parameter determines
    the depth of the tree.
    :return: The Collatz reverse binary graph as data frame.
    """
    graph_frame = create_reverse_graph(
        start_value, k=3, successor_count=successor_count,
        iteration_count=iteration_count)

    # Remove leaf nodes
    graph_frame = graph_frame[graph_frame["successor"] % 3 > 0]

    # Transform nodes
    predecessors_unique = list(graph_frame["predecessor"].unique())
    dutch_frame = None

    for pred in predecessors_unique:
        current_frame = graph_frame[graph_frame["predecessor"] == pred]
        successors = list(current_frame["successor"])

        if len(successors) > 0:
            new_predecessors = [pred]
            new_successors = [successors[0]]

            if len(successors) > 1:
                for s_i in range(0, len(successors) - 1):
                    new_predecessors.append(successors[s_i])
                    new_successors.append(successors[s_i + 1])

            new_frame = pd.DataFrame({
                "predecessor": new_predecessors,
                "successor": new_successors
            })

            if dutch_frame is None:
                dutch_frame = new_frame
            else:
                dutch_frame = dutch_frame.append(new_frame, ignore_index=True)

    return dutch_frame
