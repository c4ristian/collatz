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


def test_get_odd_predecessor_generalised():
    """
    Test case for the method get_odd_predecessors_generalised.
    :return: None
    """
    # Test k=3
    assert graph.get_odd_predecessor_generalised(1, 0) == 1
    assert graph.get_odd_predecessor_generalised(1, 1) == 5
    assert graph.get_odd_predecessor_generalised(5, 0) == 3
    assert graph.get_odd_predecessor_generalised(5, 1) == 13
    assert graph.get_odd_predecessor_generalised(5, 2) == 53
    assert graph.get_odd_predecessor_generalised(7, 5) == 9557

    assert graph.get_odd_predecessor_generalised(3, 0) is None
    assert graph.get_odd_predecessor_generalised(27, 5) is None

    # Test k=1
    assert graph.get_odd_predecessor_generalised(1, 0, k=1) is None

    # Test k=5
    assert graph.get_odd_predecessor_generalised(13, 0, k=5) == 5
    assert graph.get_odd_predecessor_generalised(13, 1, k=5) == 83
    assert graph.get_odd_predecessor_generalised(33, 0, k=5) == 13
    assert graph.get_odd_predecessor_generalised(83, 0, k=5) == 33
    assert graph.get_odd_predecessor_generalised(7, 0, k=5) == 11
    assert graph.get_odd_predecessor_generalised(11, 4, k=5) == 2306867
    assert graph.get_odd_predecessor_generalised(5, 0, k=5) is None

    # Test k=7
    assert graph.get_odd_predecessor_generalised(7, 0, k=7) is None
    assert graph.get_odd_predecessor_generalised(13, 0, k=7) is None
    assert graph.get_odd_predecessor_generalised(1243, 0, k=7) == 355
    assert graph.get_odd_predecessor_generalised(23, 0, k=7) == 13
    assert graph.get_odd_predecessor_generalised(23, 1, k=7) == 105
    assert graph.get_odd_predecessor_generalised(309, 0, k=7) == 353

    # Test k=9
    assert graph.get_odd_predecessor_generalised(9, 0, k=9) is None
    assert graph.get_odd_predecessor_generalised(25, 0, k=9) == 11
    assert graph.get_odd_predecessor_generalised(704573136177653249, 0, k=9) == 626287232157913999
    assert graph.get_odd_predecessor_generalised(1, 0, k=9) == 7
    assert graph.get_odd_predecessor_generalised(10247, 1, k=9) == 145735

    # Test k=181
    assert graph.get_odd_predecessor_generalised(1177, 0, k=181) == 13
    assert graph.get_odd_predecessor_generalised(1177, 1, k=181) == \
           19930908857449184378870435922164794575903380627735908963

    # Test if big integers are handled correctly
    assert graph.get_odd_predecessor_generalised(
        386533140549008498277345847324215954526580641501, 0, k=3) == 9 ** 50

    assert graph.get_odd_predecessor_generalised(
        966332851372521245693364618310539886316451603753, 0, k=5) == \
           386533140549008498277345847324215954526580641501

    assert graph.get_odd_predecessor_generalised(
        211385311237739022495423510255430600131723788321, 1, k=7) == \
           966332851372521245693364618310539886316451603753

    # Test exceptions
    with pytest.raises(AssertionError):
        graph.get_odd_predecessor_generalised(5.5, 0)

    with pytest.raises(AssertionError):
        graph.get_odd_predecessor_generalised(-5, 4)


def test_get_right_sibling():
    """
    Test case for the method get_right_sibling.
    :return: None.
    """
    # Test k=1
    assert graph.get_right_sibling(1, 0, k=1) == 3
    assert graph.get_right_sibling(1, 1, k=1) == 7
    assert graph.get_right_sibling(13, 3, k=1) == 223

    # Test k=3
    assert graph.get_right_sibling(1, 0) == 5
    assert graph.get_right_sibling(1, 1) == 21
    assert graph.get_right_sibling(1, 2) == 85
    assert graph.get_right_sibling(1, 99) == \
           2142584059011987034055949456454883470029603991710390447068501

    assert graph.get_right_sibling(35, 3) == 9045

    # Test k=5
    assert graph.get_right_sibling(5, 0, k=5) == 5 * 16 + 3
    assert graph.get_right_sibling(83, 10, k=5) == 1463669878895411

    # Test k=7
    assert graph.get_right_sibling(3, 0, k=7) == 25
    assert graph.get_right_sibling(3, 20, k=7) == 28987740687257866825

    # Test k=9
    assert graph.get_right_sibling(101, 0, k=9) == 6471
    assert graph.get_right_sibling(101, 20, k=9) == \
           8601582052723722270879747021191918678471

    # Test k=181
    assert graph.get_right_sibling(13, 0, k=181) == \
           19930908857449184378870435922164794575903380627735908963

    assert graph.get_right_sibling(
        13, 0, k=181, max_iterations=100) is None

    # Test exceptions
    with pytest.raises(AssertionError):
        graph.get_right_sibling(5.5, 0)

    with pytest.raises(AssertionError):
        graph.get_right_sibling(-5, 4)


def test_create_collatz_graph():
    """
    Test case for the method create_collatz_graph.
    :return: None.
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


def test_get_odd_binary_predecessors():
    """
    Test case for the method get_odd_binary_predecessors.
    :return:
    """
    assert graph.get_odd_binary_predecessors(3) == []
    assert graph.get_odd_binary_predecessors(1) == [5, 1]
    assert graph.get_odd_binary_predecessors(5) == [85, 13]
    assert graph.get_odd_binary_predecessors(85) == [341, 113]
    assert graph.get_odd_binary_predecessors(53) == [853, 35]
    assert graph.get_odd_binary_predecessors(301) == [1205, 401]
    assert graph.get_odd_binary_predecessors(17) == [277, 11]

    big_node = 8804313965977148737999987199276873995423660424042251
    assert graph.get_odd_binary_predecessors(big_node) == [big_node * 4 + 1, 11 ** 50]

    # Test exceptions
    with pytest.raises(AssertionError):
        graph.get_odd_binary_predecessors(5.5)

    with pytest.raises(AssertionError):
        graph.get_odd_binary_predecessors(-5)


def test_create_dutch_graph():
    """
    Test case for the method create_dutch_graph.
    :return:
    """
    # Root node = 1
    graph_frame = graph.create_dutch_graph(
        1, iteration_count=6)

    assert graph_frame is not None

    # Test root node of tree
    assert graph_frame["predecessor"][0] == 5
    assert graph_frame["successor"][0] == 1
    assert graph_frame["predecessor"][1] == 1
    assert graph_frame["successor"][1] == 1

    # Test v=5
    sub_frame = graph_frame[graph_frame["successor"] == 5]
    assert len(sub_frame) == 2
    assert list(sub_frame["successor"]) == [5, 5]
    assert list(sub_frame["predecessor"]) == [85, 13]

    # Test v=85
    sub_frame = graph_frame[graph_frame["successor"] == 85]
    assert list(sub_frame["predecessor"]) == [341, 113]

    # Test v=53
    sub_frame = graph_frame[graph_frame["successor"] == 53]
    assert list(sub_frame["predecessor"]) == [853, 35]

    # Test v=301
    sub_frame = graph_frame[graph_frame["successor"] == 301]
    assert list(sub_frame["predecessor"]) == [1205, 401]

    # Root node = 13
    graph_frame = graph.create_dutch_graph(
        13, iteration_count=6)

    # Test root node of tree
    assert graph_frame["successor"][0] == 13
    assert graph_frame["predecessor"][0] == 53
    assert graph_frame["successor"][1] == 13
    assert graph_frame["predecessor"][1] == 17

    # Test v=17
    sub_frame = graph_frame[graph_frame["successor"] == 17]
    assert list(sub_frame["predecessor"]) == [277, 11]

    # Big root node
    graph_frame = graph.create_dutch_graph(
        8804313965977148737999987199276873995423660424042251,
        iteration_count=1)

    assert graph_frame["successor"][1] == \
           8804313965977148737999987199276873995423660424042251
    assert graph_frame["predecessor"][1] == 11**50

    # Test empty tree
    graph_frame = graph.create_dutch_graph(
        3, iteration_count=4)

    assert graph_frame is not None
    assert len(graph_frame) == 0


def test_get_pruned_binary_predecessors():
    """
    Test case for the method get_pruned_binary_predecessors.
    :return: None.
    """
    # Pruning level 0
    pred = graph.get_pruned_binary_predecessors(1, 0)
    assert pred[0] == 5
    assert pred[1] == 1

    pred = graph.get_pruned_binary_predecessors(5, 0)
    assert pred[0] == 85
    assert pred[1] == 13

    # Pruning level 1
    pred = graph.get_pruned_binary_predecessors(5, 1)
    assert pred[0] == 85
    assert pred[1] == 5

    pred = graph.get_pruned_binary_predecessors(85, 1)
    assert pred[0] == 341
    assert pred[1] == 53

    # Pruning level 2
    pred = graph.get_pruned_binary_predecessors(341, 2)
    assert pred[0] == 5461
    assert pred[1] == 853

    pred = graph.get_pruned_binary_predecessors(853, 2)
    assert pred[0] == 3413
    assert pred[1] == 1109

    # Pruning level 3
    pred = graph.get_pruned_binary_predecessors(116053, 3)
    assert pred[0] == 464213
    assert pred[1] == 77141

    # Illegal starting nodes
    with pytest.raises(AssertionError):
        graph.get_pruned_binary_predecessors(2, 5)

    with pytest.raises(AssertionError):
        graph.get_pruned_binary_predecessors(9, 0)

    with pytest.raises(AssertionError):
        graph.get_pruned_binary_predecessors(1.6, 1)


def test_get_pruned_binary_node():
    """
    Test case for the method get_pruned_binary_node.
    :return: None.
    """
    # Pruning level 0
    node = graph.get_pruned_binary_node(1, 0)
    assert node == 1

    node = graph.get_pruned_binary_node(5, 0)
    assert node == 5

    # Pruning level 5
    node = graph.get_pruned_binary_node(113, 5)
    assert node == 7427413

    # Pruning level 100
    node = graph.get_pruned_binary_node(1, 50)
    assert node == 1902996923607946508077714625932660181843662165


def test_create_pruned_dutch_graph():
    """
    Test case for the method create_pruned_dutch_graph.
    :return: None.
    """
    # Pruning level 0
    graph_frame = graph.create_pruned_dutch_graph(
        pruning_level=0, iteration_count=3)

    assert graph_frame is not None

    # Test v=5
    sub_frame = graph_frame[graph_frame["successor"] == 5]
    assert len(sub_frame) == 2
    assert list(sub_frame["successor"]) == [5, 5]
    assert list(sub_frame["predecessor"]) == [85, 13]

    # Pruning level 1
    graph_frame = graph.create_pruned_dutch_graph(
        pruning_level=1, iteration_count=3)

    assert graph_frame is not None

    # Test v=85
    sub_frame = graph_frame[graph_frame["successor"] == 85]
    assert len(sub_frame) == 2
    assert list(sub_frame["successor"]) == [85, 85]
    assert list(sub_frame["predecessor"]) == [341, 53]

    # Test v=853
    sub_frame = graph_frame[graph_frame["successor"] == 853]
    assert len(sub_frame) == 2
    assert list(sub_frame["successor"]) == [853, 853]
    assert list(sub_frame["predecessor"]) == [3413, 565]

    # Pruning level 4
    graph_frame = graph.create_pruned_dutch_graph(
        pruning_level=4, iteration_count=3)

    assert graph_frame is not None

    # Test v=349525
    sub_frame = graph_frame[graph_frame["successor"] == 349525]
    assert len(sub_frame) == 2
    assert list(sub_frame["successor"]) == [349525, 349525]
    assert list(sub_frame["predecessor"]) == [1398101, 464213]

    # Pruning level 5
    graph_frame = graph.create_pruned_dutch_graph(
        pruning_level=5, iteration_count=3)

    sub_frame = graph_frame[graph_frame["successor"] == 21845]
    assert len(sub_frame) == 2
    assert list(sub_frame["successor"]) == [21845, 21845]
    assert list(sub_frame["predecessor"]) == [349525, 21845]

    assert graph_frame is not None

    # Pruning level 30
    graph_frame = graph.create_pruned_dutch_graph(
        pruning_level=30, iteration_count=3)

    assert graph_frame is not None

    sub_frame = graph_frame[graph_frame["successor"] == 1650586719047173699865498965]
    assert len(sub_frame) == 2
    assert list(sub_frame["successor"]) == [
        1650586719047173699865498965, 1650586719047173699865498965]

    assert list(sub_frame["predecessor"]) == [
        6602346876188694799461995861, 1650586719047173699865498965]
