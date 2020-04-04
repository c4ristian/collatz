"""
This module contains test cases for the module collatz.commons.
"""

# Imports
import numpy as np
from collatz import commons as com


def test_collatz_sequence():
    """
    Test case for the method collatz_sequence.
    :return: None
    """
    # Test different sequences
    result = com.collatz_sequence(1)
    assert result == [1, 4, 2, 1], "Result should be 1"

    result = com.collatz_sequence(10)
    assert result == [10, 5, 16, 8, 4, 2, 1], "Result not expected"

    result = com.collatz_sequence(64)
    assert result == [64, 32, 16, 8, 4, 2, 1], "Result should be one"

    result = com.collatz_sequence(13, 5)
    assert result == [
        13, 66, 33, 166, 83, 416, 208, 104, 52, 26, 13], "Result should be one"

    # Test if parameter max_iterations is applied
    result = com.collatz_sequence(7, k=5, max_iterations=5)
    assert result == [7, 36, 18, 9, 46, 23]

    # Test if algorithm stops in case of a cycle
    result = com.collatz_sequence(13, k=5, max_iterations=150)
    assert result == [13, 66, 33, 166, 83, 416, 208, 104, 52, 26, 13]

    result = com.collatz_sequence(5, k=5, max_iterations=150)
    assert result == [5, 26, 13, 66, 33, 166, 83, 416, 208, 104, 52, 26]

    # Should not accept numbers smaller than 1
    try:
        com.collatz_sequence(0)
        assert False, "Exception expected"
    except AssertionError:
        pass

    # Should only accept whole numbers
    try:
        com.next_collatz_number(0.25)
        assert False, "Exception expected"
    except AssertionError:
        pass


def test_next_collatz_number():
    """
    Test case for the method next_collatz_number.
    :return: None
    """
    assert com.next_collatz_number(1) == 4, "Result should be 1"
    assert com.next_collatz_number(3) == 10, "Result should be 10"
    assert com.next_collatz_number(3, 5) == 16, "Result should be 16"
    assert com.next_collatz_number(4) == 2, "Result should be 2"
    assert com.next_collatz_number(10) == 5, "Result should be 5"
    assert com.next_collatz_number(5, 5) == 26, "Result should be 5"

    # Should not accept numbers smaller than 1
    try:
        com.next_collatz_number(0)
        assert False, "Exception expected"
    except AssertionError:
        pass

    # Should only accept whole numbers
    try:
        com.next_collatz_number(0.25)
        assert False, "Exception expected"
    except AssertionError:
        pass

    try:
        com.next_collatz_number("abc")
        assert False, "Exception expected"
    except TypeError:
        pass


def test_next_odd_collatz_number():
    """
    Test case for the method next_collatz_number.
    :return: None
    """
    assert com.next_odd_collatz_number(1) == 1, "Result should be 1"
    assert com.next_odd_collatz_number(3) == 5, "Result should be 10"
    assert com.next_odd_collatz_number(3, 5) == 1, "Result should be 16"
    assert com.next_odd_collatz_number(4) == 1, "Result should be 2"
    assert com.next_odd_collatz_number(10) == 5, "Result should be 5"
    assert com.next_odd_collatz_number(5, 5) == 13, "Result should be 13"
    assert com.next_odd_collatz_number(33, 5) == 83, "Result should be 83"
    assert com.next_odd_collatz_number(5, 2) == 11, "Result should be 83"

    # Should not accept numbers smaller than 1
    try:
        com.next_odd_collatz_number(0)
        assert False, "Exception expected"
    except AssertionError:
        pass

    # Should only accept whole numbers
    try:
        com.next_odd_collatz_number(0.25)
        assert False, "Exception expected"
    except AssertionError:
        pass

    try:
        com.next_odd_collatz_number("abc")
        assert False, "Exception expected"
    except TypeError:
        pass


def test_analyse_collatz_basic_attributes():
    """
    Test case for the method analyse_collatz_basic_attributes
    :return: None
    """
    # Test empty sequence
    test_sequence = []
    analysis_frame = com.analyse_collatz_basic_attributes(test_sequence)

    assert analysis_frame is not None, "result should not be None"
    assert analysis_frame.empty, "result should be an empty data frame"

    # Test sequence for 1
    test_sequence = [1]
    analysis_frame = com.analyse_collatz_basic_attributes(test_sequence)

    assert analysis_frame is not None, "result should not be None"
    assert not analysis_frame.empty, "result should not be empty"
    assert len(analysis_frame) == 1

    series = analysis_frame.iloc[0]
    assert series["collatz"] == 1
    assert series["odd"] == 1
    assert series["log2"] == 0

    # Test sequence for several elements
    test_sequence = [10, 5, 16, 8, 4, 2, 1]
    analysis_frame = com.analyse_collatz_basic_attributes(test_sequence)

    assert analysis_frame is not None, "result should not be None"
    assert not analysis_frame.empty, "result should not be empty"
    assert len(analysis_frame) == 7

    assert list(analysis_frame["collatz"]) == test_sequence
    assert list(analysis_frame["odd"]) == [0, 1, 0, 0, 0, 0, 1]
    assert list(analysis_frame["log2"]) == list(np.log2(test_sequence))
    assert list(analysis_frame["log2_fraction"]) == list(np.log2(test_sequence) % 1)


def test_analyse_collatz_binary_attributes():
    """
    Test case for the method analyse_collatz_basic_attributes
    :return: None
    """
    test_sequence = [10, 5, 16, 8, 4, 2, 1]
    analysis_frame = com.analyse_collatz_binary_attributes(test_sequence)

    assert analysis_frame is not None, "result should not be None"
    assert not analysis_frame.empty, "result should not be empty"
    assert len(analysis_frame) == 7

    assert list(analysis_frame["collatz"]) == test_sequence
    assert list(analysis_frame["bin_tz"]) == [1, 0, 4, 3, 2, 1, 0]
    assert list(analysis_frame["bin_len"]) == [4, 3, 5, 4, 3, 2, 1]
    assert analysis_frame["bin_str"][0] == "1010"
    assert analysis_frame["bin_str"][1] == "101"
    assert analysis_frame["bin_str"][2] == "10000"


def test_trailing_zeros():
    """
    Test case for the method trailing_zeros.
    :return: None
    """
    assert com.trailing_zeros(1) == 0, "0 expected"
    assert com.trailing_zeros(2) == 1, "1 expected"
    assert com.trailing_zeros(3) == 0, "0 expected"
    assert com.trailing_zeros(8) == 3, "3 expected"
    assert com.trailing_zeros(668503069687808) == 45, "45 expected"

    # Should only accept whole numbers
    try:
        com.next_collatz_number(0.25)
        assert False, "Exception expected"
    except AssertionError:
        pass


def test_to_binary():
    """
    Test case for the method to_binary.
    :return: None
    """
    assert com.to_binary(0) == "0", "different value expected"
    assert com.to_binary(1) == "1", "different value expected"
    assert com.to_binary(5) == "101", "different value expected"
    assert com.to_binary(19373728) == "1001001111001111010100000", "different value expected"

    # Should only accept integers
    try:
        com.to_binary(0.25)
        assert False, "Exception expected"
    except TypeError:
        pass
