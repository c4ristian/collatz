"""
This module contains test cases for the module collatz.cycles.
"""

# Imports
from collatz import cycles


def test_should_find_cycles_correctly():
    """
    Test case for the method find_cycles.
    :return: None.
    """
    # Check cycles for k=1
    result = cycles.find_cycles(1, 1, 1)
    assert result == [[1, 1]]

    result = cycles.find_cycles(1, 2, 1)
    assert not result

    # Check cycles for k=2
    result = cycles.find_cycles(2, 1, 10000)
    assert not result

    # Check cycles for k=3
    result = cycles.find_cycles(3, 1, 1)
    assert result == [[1, 1]]

    result = cycles.find_cycles(3, 4, 1)
    assert not result

    # Check cycles for k=5
    result = cycles.find_cycles(5, 1, 101)
    assert not result

    result = cycles.find_cycles(5, 2, 101)
    assert result == [[1, 3, 1]]

    result = cycles.find_cycles(5, 3, 101)
    assert result == [[13, 33, 83, 13], [17, 43, 27, 17]]

    # Check cycles for k=181
    result = cycles.find_cycles(181, 2, 101)
    assert result == [[27, 611, 27], [35, 99, 35]]

    result = cycles.find_cycles(181, 3, 101)
    assert not result


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
