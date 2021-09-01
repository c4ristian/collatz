"""
This module contains test cases for the module collatz.tensor.
"""
import numpy as np
import tensorflow as tf
from collatz import tensor as tc


def test_next_even_collatz_numbers():
    """
    Testcase for the method next_even_collatz_numbers.

    :return: None.
    """
    # Test empty list
    odds_np = np.array([])
    odds = tf.constant(odds_np, dtype=tf.int64)

    evens = tc.next_even_collatz_numbers(odds)
    assert list(evens) == list(odds)

    # Test default case
    odds_np = np.array([1, 3, 5])
    odds = tf.constant(odds_np, dtype=tf.int64)

    evens = tc.next_even_collatz_numbers(odds)
    assert list(evens) == list(odds_np * 3 + 1)

    odds_np = np.array(range(1, 1001 + 1))
    odds = tf.constant(odds_np, dtype=tf.int64)

    evens = tc.next_even_collatz_numbers(odds, k=5, c=3)
    assert list(evens) == list(odds_np * 5 + 3)

    # Test negative values
    odds_np = np.array([-1])
    odds = tf.constant(odds_np, dtype=tf.int64)

    # Test different k and c
    evens = tc.next_even_collatz_numbers(odds, k=5, c=3)
    assert list(evens) == list(odds_np * 5 + 3)

    # Test without tensor
    odds = [1, 2, 3]

    evens = tc.next_even_collatz_numbers(odds, k=7, c=5)
    assert list(evens) == list(np.array(odds) * 7 + 5)


def test_next_odd_collatz_numbers():
    """
    Testcase for the method next_odd_collatz_numbers.

    :return: None.
    """
    # Test empty list
    evens_np = np.array([])
    evens = tf.constant(evens_np, dtype=tf.int64)

    odds = tc.next_odd_collatz_numbers(evens)
    assert list(odds) == list(evens)

    # Test default case
    evens_np = [4, 10, 16]
    evens = tf.constant(evens_np, dtype=tf.int64)

    odds = tc.next_odd_collatz_numbers(evens)
    assert list(odds) == [1, 5, 1]

    # Test negative numbers
    evens_np = [32, -10, 22]
    evens = tf.constant(evens_np, dtype=tf.int64)

    odds = tc.next_odd_collatz_numbers(evens)
    assert list(odds) == [1, -5, 11]


def test_trailing_zeros():
    """
    Testcase for the method trailing_zeros.

    :return: None.
    """
    # Empty list
    assert tc.trailing_zeros([]) == []

    # Default cases
    assert list(tc.trailing_zeros([10, 16, 11])) == [1, 4, 0]
    assert list(tc.trailing_zeros(np.array([32, -2, -20]))) == [5, 1, 2]
