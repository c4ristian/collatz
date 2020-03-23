"""
This module contains test cases for the module collatz.graph.
"""

from collatz import graph


def test_get_odd_predecessor():
    """
    Test case for the method get_odd_predecessors.
    :return: None
    """
    # Test k=3
    assert graph.get_odd_predecessor(1, 0) == 1
    assert graph.get_odd_predecessor(1, 1) == 5
    assert graph.get_odd_predecessor(5, 0) == 3
    assert graph.get_odd_predecessor(5, 1) == 13
    assert graph.get_odd_predecessor(5, 2) == 53
    assert graph.get_odd_predecessor(7, 5) == 9557

    assert graph.get_odd_predecessor(
        11, 3) == graph.get_odd_predecessors(11)[0][3]

    assert graph.get_odd_predecessor(
        19291, 5) == graph.get_odd_predecessors(19291)[0][5]

    assert graph.get_odd_predecessor(3, 0) is None
    assert graph.get_odd_predecessor(27, 5) is None

    # Test k=1 and k=5
    assert graph.get_odd_predecessor(1, 0, k=1) == 1
    assert graph.get_odd_predecessor(1, 1, k=1) == 3
    assert graph.get_odd_predecessor(7, 2, k=1) == 55
    assert graph.get_odd_predecessor(13, 0, k=5) == 5
    assert graph.get_odd_predecessor(13, 1, k=5) == 83
    assert graph.get_odd_predecessor(33, 0, k=5) == 13
    assert graph.get_odd_predecessor(83, 0, k=5) == 33
    assert graph.get_odd_predecessor(7, 0, k=5) == 11
    assert graph.get_odd_predecessor(11, 4, k=5) == 2306867
    assert graph.get_odd_predecessor(5, 0, k=5) is None

    # Test exceptions
    try:
        graph.get_odd_predecessor(5.5, 0)
        assert False, "AssertionError expected"
    except AssertionError:
        pass

    try:
        graph.get_odd_predecessor(-5, 4)
        assert False, "AssertionError expected"
    except AssertionError:
        pass

    try:
        graph.get_odd_predecessor(5, 4, k=7)
        assert False, "TypeError expected"
    except TypeError:
        pass


def test_get_odd_predecessors():
    """
    Test case for the method get_odd_predecessors.
    :return: None
    """
    assert list(graph.get_odd_predecessors(
        1)[0]) == [1, 5, 21, 85, 341, 1365, 5461, 21845, 87381, 349525]

    assert list(graph.get_odd_predecessors(
        1)[1]) == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    assert list(graph.get_odd_predecessors(
        5, power_range=range(1, 6))[0]) == [3, 13, 53]

    assert list(graph.get_odd_predecessors(
        5, power_range=range(1, 6))[1]) == [1, 3, 5]

    assert list(graph.get_odd_predecessors(
        13, k=5, power_range=range(1, 10))[0]) == [5, 83, 1331]

    assert list(graph.get_odd_predecessors(
        3, k=3, power_range=range(1, 10))[0]) == []

    assert list(graph.get_odd_predecessors(
        3, k=3, power_range=range(1, 10))[1]) == []

    assert list(graph.get_odd_predecessors(
        10, k=3, power_range=range(1, 10))[0]) == [13, 53, 213, 853]

    # Fixme: This result is not correct
    assert list(graph.get_odd_predecessors(
        180618717, k=7, power_range=range(1, 31))[0]) == [3463176261430711]

    try:
        graph.get_odd_predecessors(5.5)
        assert False, "AssertionError expected"
    except AssertionError:
        pass

    try:
        graph.get_odd_predecessors(-5)
        assert False, "AssertionError expected"
    except AssertionError:
        pass


def test_create_collatz_graph():
    """
    Test case for the method create_collatz_graph.
    :return:
    """
    graph_frame = graph.create_collatz_graph(
        1, k=3, predecessor_count=5, iteration_count=1)

    assert graph_frame is not None
    assert len(graph_frame) == 5
    assert set(graph_frame["successor"]) == {1}
    assert set(graph_frame["iteration"]) == {1}
    assert list(graph_frame["predecessor"]) == [1, 5, 21, 85, 341]

    graph_frame = graph.create_collatz_graph(
        1, k=3, predecessor_count=5, iteration_count=2)

    assert len(graph_frame) == 20
    assert set(graph_frame["successor"]) == {1, 5, 85, 341}

    graph_frame = graph.create_collatz_graph(
        1, k=1, predecessor_count=2, iteration_count=3)

    assert len(graph_frame) == 8
    assert set(graph_frame["successor"]) == {1, 3, 5, 11}
    assert list(graph_frame["predecessor"]) == [1, 3, 5, 11, 9, 19, 21, 43]
