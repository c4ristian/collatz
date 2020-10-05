"""
This module contains test cases for the module collatz.graph.
"""

import pytest
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

    # Test k=7
    assert graph.get_odd_predecessor(7, 0, k=7) is None
    assert graph.get_odd_predecessor(13, 0, k=7) is None
    assert graph.get_odd_predecessor(1243, 0, k=7) == 355
    assert graph.get_odd_predecessor(23, 0, k=7) == 13
    assert graph.get_odd_predecessor(23, 1, k=7) == 105
    assert graph.get_odd_predecessor(309, 0, k=7) == 353

    # Test k=9
    assert graph.get_odd_predecessor(9, 0, k=9) is None
    assert graph.get_odd_predecessor(25, 0, k=9) == 11
    assert graph.get_odd_predecessor(704573136177653249, 0, k=9) == 626287232157913999
    assert graph.get_odd_predecessor(1, 0, k=9) == 7
    assert graph.get_odd_predecessor(10247, 1, k=9) == 145735

    # Test if big integers are handled correctly
    assert graph.get_odd_predecessor(
        386533140549008498277345847324215954526580641501, 0, k=3) == 9**50

    assert graph.get_odd_predecessor(
        966332851372521245693364618310539886316451603753, 0, k=5) == \
           386533140549008498277345847324215954526580641501

    assert graph.get_odd_predecessor(
        211385311237739022495423510255430600131723788321, 1, k=7) == \
           966332851372521245693364618310539886316451603753

    # Test exceptions
    with pytest.raises(AssertionError):
        graph.get_odd_predecessor(5.5, 0)

    with pytest.raises(AssertionError):
        graph.get_odd_predecessor(-5, 4)

    with pytest.raises(TypeError):
        graph.get_odd_predecessor(5, 4, k=11)


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

    graph_frame = graph.create_collatz_graph(
        386533140549008498277345847324215954526580641501,
        k=3, predecessor_count=1, iteration_count=1)

    assert len(graph_frame) == 1
    assert graph_frame["successor"][0] == 386533140549008498277345847324215954526580641501
    assert graph_frame["predecessor"][0] == 9**50


def test_create_reverse_graph():
    """
    Test case for the method create_reverse_graph.
    :return:
    """
    graph_frame = graph.create_reverse_graph(
        1, k=3, successor_count=5, iteration_count=1)

    assert graph_frame is not None
    assert len(graph_frame) == 5
    assert set(graph_frame["predecessor"]) == {1}
    assert set(graph_frame["iteration"]) == {1}
    assert list(graph_frame["successor"]) == [1, 5, 21, 85, 341]

    graph_frame = graph.create_reverse_graph(
        1, k=3, successor_count=5, iteration_count=2)

    assert len(graph_frame) == 20
    assert set(graph_frame["predecessor"]) == {1, 5, 85, 341}

    graph_frame = graph.create_reverse_graph(
        1, k=1, successor_count=2, iteration_count=3)

    assert len(graph_frame) == 8
    assert set(graph_frame["predecessor"]) == {1, 3, 5, 11}
    assert list(graph_frame["successor"]) == [1, 3, 5, 11, 9, 19, 21, 43]

    graph_frame = graph.create_reverse_graph(
        386533140549008498277345847324215954526580641501,
        k=3, successor_count=1, iteration_count=1)

    assert len(graph_frame) == 1
    assert graph_frame["predecessor"][0] == 386533140549008498277345847324215954526580641501
    assert graph_frame["successor"][0] == 9 ** 50


def test_create_dutch_graph():
    """
    Test case for the method create_dutch_graph.
    :return:
    """
    # Root node = 1
    graph_frame = graph.create_dutch_graph(
        1, successor_count=5, iteration_count=4)

    assert graph_frame is not None

    # Test root node of tree
    assert graph_frame["predecessor"][0] == 1
    assert graph_frame["successor"][0] == 1
    assert graph_frame["predecessor"][1] == 1
    assert graph_frame["successor"][1] == 5

    # Test v=5
    sub_frame = graph_frame[graph_frame["predecessor"] == 5]
    assert len(sub_frame) == 2
    assert list(sub_frame["predecessor"]) == [5, 5]
    assert list(sub_frame["successor"]) == [85, 13]

    # Test v=85
    sub_frame = graph_frame[graph_frame["predecessor"] == 85]
    assert list(sub_frame["successor"]) == [341, 113]

    # Test v=53
    sub_frame = graph_frame[graph_frame["predecessor"] == 53]
    assert list(sub_frame["successor"]) == [853, 35]

    # Test v=301
    sub_frame = graph_frame[graph_frame["predecessor"] == 301]
    assert list(sub_frame["successor"]) == [1205, 401]

    # Root node = 13
    graph_frame = graph.create_dutch_graph(
        13, successor_count=4, iteration_count=4)

    # Test root node of tree
    assert graph_frame["predecessor"][0] == 13
    assert graph_frame["successor"][0] == 17
    assert graph_frame["predecessor"][1] == 17
    assert graph_frame["successor"][1] == 277

    # Test v=17
    sub_frame = graph_frame[graph_frame["predecessor"] == 17]
    assert list(sub_frame["successor"]) == [277, 11]

    # Big root node
    graph_frame = graph.create_dutch_graph(
        8804313965977148737999987199276873995423660424042251,
        successor_count=1, iteration_count=1)

    assert graph_frame["predecessor"][0] == \
           8804313965977148737999987199276873995423660424042251
    assert graph_frame["successor"][0] == 11**50

    # Test empty tree
    graph_frame = graph.create_dutch_graph(
        3, successor_count=4, iteration_count=4)

    assert graph_frame is not None
    assert len(graph_frame) == 0
