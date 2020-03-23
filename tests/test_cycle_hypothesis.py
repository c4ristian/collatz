"""
This file contains methods that test the hypothesis that
collatz sequences cannot end in cycles.
"""

# Imports
from math import log2
import itertools
import numpy as np
import pandas as pd


def _fraction(x, k=3):
    factor = 2**(int(log2(k)))
    result = k/factor + 1/(factor*x)
    return result


def test_falsify_k_3():
    """
    This method tests that the hypothesis is not falsifiable for k=3
    :return:
    """
    k = 3

    # There should be a cycle for 1 with length 1
    assert _fraction(1, k) == 2

    # There shouldn't be a cycle with length 2 or greater
    assert _fraction(3, k) * _fraction(5, k) > 2
    assert _fraction(100001, k) * _fraction(100003, k) > 2
    assert 1.5**2 > 2
    assert 1.5**3 > 2


def test_falsify_k_5():
    """
    This method tests that the hypothesis is not falsifiable for k=5
    :return:
    """
    k = 5

    # There should be a cycle for 1 with length 1
    assert _fraction(1, k) < 2

    # There should be cycle for length 2 and 3
    assert _fraction(1, k) * _fraction(3, k) == 2
    assert _fraction(13, k) * _fraction(33, k) * _fraction(83, k) == 2
    assert _fraction(17, k) * _fraction(43, k) * _fraction(27, k) == 2

    # There should not be a cycle for length 4
    assert 1.25**4 > 2

    x = np.array(range(1, 101, 2))
    fractions = _fraction(x, k)

    permutations = list(itertools.product(
        fractions, fractions, fractions, fractions))

    x_frame = pd.DataFrame(
        permutations, columns=["x1", "x2", "x3", "x4"])

    x_frame["prod"] = x_frame.prod(axis=1)
    assert set(x_frame["prod"] > 2) == {True}


def test_falsify_k_7():
    """
    This method tests that the hypothesis is not falsifiable for k=7
    :return:
    """
    k = 7

    # There should be a cycle for 1 with length 1
    assert _fraction(1, k) == 2

    # There should not be cycles for length 2 and 3
    assert 1.75**2 > 2
    assert 1.75**3 > 2

    x = np.array(range(1, 5001, 2))
    fractions = _fraction(x, k)

    permutations = list(itertools.product(
        fractions, fractions))

    x_frame = pd.DataFrame(
        permutations, columns=["x1", "x2"])

    x_frame["prod"] = x_frame.prod(axis=1)
    assert set(x_frame["prod"] > 2) == {True}


def test_falsify_k_13():
    """
    This method tests that the hypothesis is not falsifiable for k=13
    :return:
    """
    k = 13

    # There should be a cycle for 1 with length 1
    assert _fraction(1, k) != 2

    # There should not be cycles for length 2 and 3
    assert 1.625**2 > 2
    assert 1.625**3 > 2

    x = np.array(range(1, 5001, 2))
    fractions = _fraction(x, k)

    permutations = list(itertools.product(
        fractions, fractions))

    x_frame = pd.DataFrame(
        permutations, columns=["x1", "x2"])

    x_frame["prod"] = x_frame.prod(axis=1)
    assert set(x_frame["prod"] > 2) == {True}


def test_falsify_k_15():
    """
    This method tests that the hypothesis is not falsifiable for k=15
    :return:
    """
    k = 15

    # There should be a cycle for 1 with length 1
    assert _fraction(1, k) == 2

    # There should not be cycles for length 2 and 3
    assert (15/8) ** 2 > 2
    assert (15/8) ** 3 > 2


def test_falsify_k_181():
    """
    This method tests that the hypothesis is not falsifiable for k=181
    :return:
    """
    k = 181

    # There should be a cycle for 1 with length 1
    assert _fraction(1, k) < 2

    # There should be cycle for length 2
    assert _fraction(27, k) * _fraction(611, k) == 2
    assert _fraction(35, k) * _fraction(99, k) == 2

    # There should not be a cycle for length 3
    assert (181/2**7) ** 3 > 2

    x = np.array(range(1, 101, 2))
    fractions = _fraction(x, k)

    permutations = list(itertools.product(
        fractions, fractions, fractions))

    x_frame = pd.DataFrame(
        permutations, columns=["x1", "x2", "x3"])

    x_frame["prod"] = x_frame.prod(axis=1)
    assert set(x_frame["prod"] > 2) == {True}
