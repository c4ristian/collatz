"""
This module contains test cases for the module collatz.cycles.
"""

# Imports
from collatz import cycles


def test_find_cycles():
    """
    Test case for the method find_cycles.
    :return: None.
    """
    # k=1, c=1
    result = cycles.find_cycles(
        k=1, max_c=1, max_value=101)

    assert len(result) == 1
    assert list(result["k"]) == [1]
    assert list(result["c"]) == [1]
    assert list(result["length"]) == [1]
    assert list(result["v_1"]) == [1]
    assert list(result["values"]) == ["1"]

    # k=5, c=1
    result = cycles.find_cycles(
        k=5, max_c=1, max_value=16)

    assert len(result) == 2
    assert list(result["k"]) == [5, 5]
    assert list(result["c"]) == [1, 1]
    assert list(result["length"]) == [2, 3]
    assert list(result["v_1"]) == [1, 13]
    assert list(result["values"]) == ["1,3", "13,33,83"]

    # k=3, c=3
    result = cycles.find_cycles(
        k=3, max_c=5, max_iterations=3)

    assert len(result) == 6
    assert list(result["k"]) == [3, 3, 3, 3, 3, 3]
    assert list(result["c"]) == [1, 3, 5, 5, 5, 5]
    assert list(result["length"]) == [1, 1, 1, 1, 3, 3]
    assert list(result["v_1"]) == [1, 3, 1, 5, 19, 23]

    # If no cycles are found an empty frame is returned
    result = cycles.find_cycles(k=11, max_c=1, max_iterations=3)
    assert len(result) == 0


def test_find_cycles_in_ranges():
    """
    Test case for the method find_cycles_in_ranges.
    :return: None.
    """
    # k=1, c=1
    result = cycles.find_cycles_in_ranges(
        k=range(1, 3, 2), c=range(1, 3, 2))

    assert result is not None
    assert len(result) == 1
    assert result["k"][0] == 1
    assert result["c"][0] == 1
    assert result["length"][0] == 1
    assert result["v_1"][0] == 1
    assert result["values"][0] == "1"

    # k=1, c=(3, 5)
    result = cycles.find_cycles_in_ranges(
        k=range(1, 3, 2), c=range(3, 7, 2))

    assert len(result) == 4
    assert list(result["k"]) == [1, 1, 1, 1]
    assert list(result["c"]) == [3, 3, 5, 5]
    assert list(result["length"]) == [1, 1, 2, 1]
    assert list(result["v_1"]) == [1, 3, 1, 5]

    # k=3, c=5
    result = cycles.find_cycles_in_ranges(
        k=range(3, 5), c=range(5, 7), max_iterations=3)

    assert len(result) == 4
    assert list(result["k"]) == [3, 3, 3, 3]
    assert list(result["c"]) == [5, 5, 5, 5]
    assert list(result["length"]) == [1, 1, 3, 3]
    assert list(result["v_1"]) == [1, 5, 19, 23]

    # k=(3, 5), c=1
    result = cycles.find_cycles_in_ranges(
        k=range(3, 7, 2), c=range(1, 3, 2), max_iterations=3)

    assert len(result) == 4
    assert list(result["k"]) == [3, 5, 5, 5]
    assert list(result["c"]) == [1, 1, 1, 1]
    assert list(result["length"]) == [1, 2, 3, 3]
    assert list(result["v_1"]) == [1, 1, 13, 17]
    assert list(result["values"]) == ["1", "1,3", "13,33,83", "17,43,27"]

    # If no cycles are found an empty frame is returned
    result = cycles.find_cycles_in_ranges(
        k=range(11, 13, 2), c=range(1, 3, 2), max_iterations=3)

    assert len(result) == 0


def test_should_predict_cycle_alpha_correctly():
    """
    Test case for the method predict_cycle_alpha.
    :return: None.
    """
    # k=1
    assert cycles.predict_cycle_alpha(1, 1) == 1
    assert cycles.predict_cycle_alpha(1, 17) == 1

    # k=3
    assert cycles.predict_cycle_alpha(3, 1) == 2
    assert cycles.predict_cycle_alpha(3, 2) == 4
    assert cycles.predict_cycle_alpha(3, 3) == 5

    # k=5
    assert cycles.predict_cycle_alpha(5, 1) == 3
    assert cycles.predict_cycle_alpha(5, 2) == 5
    assert cycles.predict_cycle_alpha(5, 3) == 7

    # k=7
    assert cycles.predict_cycle_alpha(7, 1) == 3

    # k=15
    assert cycles.predict_cycle_alpha(15, 1) == 4

    # k=31
    assert cycles.predict_cycle_alpha(31, 1) == 5

    # k=63
    assert cycles.predict_cycle_alpha(63, 1) == 6

    # k=127
    assert cycles.predict_cycle_alpha(127, 1) == 7

    # k=181
    assert cycles.predict_cycle_alpha(181, 1) == 8
    assert cycles.predict_cycle_alpha(181, 2) == 15
