"""
This module contains test cases for the module collatz.cycles.
"""

# Imports
from collatz import cycles


def test_should_find_cycles_correctly():
    """
    This method ensures that the module finds cycles in
    collatz sequences correctly.
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


def test_should_calculate_cycle_alpha_correctly():
    """
    This method ensures that cycle alphas are calculated
    correctly.
    :return: None.
    """
    # Simple algorithm

    # k=1
    assert cycles.calculate_cycle_alpha(1, 1) == 1
    assert cycles.calculate_cycle_alpha(1, 2) == 1
    assert cycles.calculate_cycle_alpha(1, 5) == 1

    # k=2
    assert cycles.calculate_cycle_alpha(2, 1) == 2
    assert cycles.calculate_cycle_alpha(2, 2) == 3
    assert cycles.calculate_cycle_alpha(2, 3) == 4

    # k=3
    assert cycles.calculate_cycle_alpha(3, 1) == 2
    assert cycles.calculate_cycle_alpha(3, 2) == 3
    assert cycles.calculate_cycle_alpha(3, 3) == 4

    # k=5
    assert cycles.calculate_cycle_alpha(5, 1) == 3
    assert cycles.calculate_cycle_alpha(5, 2) == 5
    assert cycles.calculate_cycle_alpha(5, 3) == 7
    assert cycles.calculate_cycle_alpha(5, 7) == 15

    # k=63
    assert cycles.calculate_cycle_alpha(63, 1) == 6

    # k=181
    assert cycles.calculate_cycle_alpha(181, 2) == 15

    # Lambda algorithm

    # k=1
    assert cycles.calculate_cycle_alpha(1, 1, "lambda") == 1
    assert cycles.calculate_cycle_alpha(1, 100, "lambda") == 1

    # k=3
    assert cycles.calculate_cycle_alpha(3, 1, "lambda") == 2
    assert cycles.calculate_cycle_alpha(3, 3, "lambda") == 4
    assert cycles.calculate_cycle_alpha(3, 4, "lambda") == 6
    assert cycles.calculate_cycle_alpha(3, 5, "lambda") == 7

    # k=5
    assert cycles.calculate_cycle_alpha(5, 1, "lambda") == 3
    assert cycles.calculate_cycle_alpha(5, 2, "lambda") == 5
    assert cycles.calculate_cycle_alpha(5, 3, "lambda") == 7
    assert cycles.calculate_cycle_alpha(5, 7, "lambda") == 16

    # Max algorithm

    # k=1
    assert cycles.calculate_cycle_alpha(1, 1, "max") == 1
    assert cycles.calculate_cycle_alpha(1, 17, "max") == 1

    # k=3
    assert cycles.calculate_cycle_alpha(3, 1, "max") == 2
    assert cycles.calculate_cycle_alpha(3, 2, "max") == 4
    assert cycles.calculate_cycle_alpha(3, 3, "max") == 5

    # k=5
    assert cycles.calculate_cycle_alpha(5, 1, "max") == 3
    assert cycles.calculate_cycle_alpha(5, 2, "max") == 5
    assert cycles.calculate_cycle_alpha(5, 3, "max") == 7

    # k=7
    assert cycles.calculate_cycle_alpha(7, 1, "max") == 3

    # k=15
    assert cycles.calculate_cycle_alpha(15, 1, "max") == 4

    # k=31
    assert cycles.calculate_cycle_alpha(31, 1, "max") == 5

    # k=63
    assert cycles.calculate_cycle_alpha(63, 1, "max") == 6

    # k=127
    assert cycles.calculate_cycle_alpha(127, 1, "max") == 7

    # k=181
    assert cycles.calculate_cycle_alpha(181, 1, "max") == 8
    assert cycles.calculate_cycle_alpha(181, 2, "max") == 15
