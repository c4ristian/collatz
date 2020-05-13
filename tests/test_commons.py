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
    assert result == [1, 4, 2, 1]

    result = com.collatz_sequence(10)
    assert result == [10, 5, 16, 8, 4, 2, 1]

    result = com.collatz_sequence(64)
    assert result == [64, 32, 16, 8, 4, 2, 1]

    result = com.collatz_sequence(13, 5)
    assert result == [
        13, 66, 33, 166, 83, 416, 208, 104, 52, 26, 13]

    result = com.collatz_sequence(5, k=5, max_iterations=150)
    assert result == [5, 26, 13, 66, 33, 166, 83, 416, 208, 104, 52, 26]

    # Test if parameter max_iterations is applied
    result = com.collatz_sequence(7, k=5, max_iterations=5)
    assert result == [7, 36, 18, 9, 46, 23]

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


def test_odd_collatz_sequence():
    """
    Test case for the method odd_collatz_sequence.
    :return: None
    """
    # Test different sequences
    result = com.odd_collatz_sequence(1)
    assert result == [1, 1]

    result = com.odd_collatz_sequence(10)
    assert result == [5, 1]

    result = com.odd_collatz_sequence(64)
    assert result == [1, 1]

    result = com.odd_collatz_sequence(13, 5)
    assert result == [13, 33, 83, 13]

    result = com.odd_collatz_sequence(5, 5)
    assert result == [5, 13, 33, 83, 13]

    # Test if parameter max_iterations is applied
    result = com.odd_collatz_sequence(7, k=5, max_iterations=5)
    assert result == [7, 9, 23, 29, 73, 183]

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
    assert com.next_collatz_number(1) == 4
    assert com.next_collatz_number(3) == 10
    assert com.next_collatz_number(3, 5) == 16
    assert com.next_collatz_number(4) == 2
    assert com.next_collatz_number(10) == 5
    assert com.next_collatz_number(5, 5) == 26

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
    assert com.next_odd_collatz_number(1) == 1
    assert com.next_odd_collatz_number(3) == 5
    assert com.next_odd_collatz_number(3, 5) == 1
    assert com.next_odd_collatz_number(4) == 1
    assert com.next_odd_collatz_number(10) == 5
    assert com.next_odd_collatz_number(5, 5) == 13
    assert com.next_odd_collatz_number(33, 5) == 83
    assert com.next_odd_collatz_number(5, 2) == 11

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


def test_odd_collatz_sequence_components():
    """
    Test case for the method odd_collatz_sequence_components.
    :return: None
    """
    # Test different sequences
    result_frame = com.odd_collatz_sequence_components(3)
    assert list(result_frame.columns) == ["n", "variable", "decimal"]
    assert list(result_frame["n"].unique()) == [1, 2, 3]
    assert list(result_frame["variable"].unique()) == ["vi", "kvi", "kvi+1"]
    assert list(result_frame["decimal"]) == [3, 9, 10, 5, 15, 16, 1]

    result_frame = com.odd_collatz_sequence_components(1, 5)
    assert list(result_frame["decimal"]) == [1, 5, 6, 3, 15, 16, 1]

    # Test if parameter max_iterations is applied
    result_frame = com.odd_collatz_sequence_components(7, k=5, max_iterations=1)
    assert list(result_frame["n"].unique()) == [1, 2]
    assert list(result_frame["decimal"]) == [7, 35, 36, 9]

    # Should not accept numbers smaller than 1
    try:
        com.odd_collatz_sequence_components(0)
        assert False, "Exception expected"
    except AssertionError:
        pass

    # Should only accept whole numbers
    try:
        com.odd_collatz_sequence_components(0.25)
        assert False, "Exception expected"
    except AssertionError:
        pass


def test_odd_collatz_components():
    """
    Test case for the method _odd_collatz_components.
    :return: None
    """
    # Test x=13 and k=3
    # pylint: disable=W0212
    comp = com._odd_collatz_components(13)
    assert comp is not None
    assert comp["vi"] == 13
    assert comp["kvi"] == 39
    assert comp["kvi+1"] == 40
    assert comp["vi_1"] == 5
    # Test x=1 and k=3
    comp = com._odd_collatz_components(1, 3)
    assert comp is not None
    assert comp["vi"] == 1
    assert comp["kvi"] == 3
    assert comp["kvi+1"] == 4
    assert comp["vi_1"] == 1
    # Test x=5 and k=1
    comp = com._odd_collatz_components(5, 1)
    assert comp is not None
    assert comp["vi"] == 5
    assert comp["kvi"] == 5
    assert comp["kvi+1"] == 6
    assert comp["vi_1"] == 3


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


def test_trailing_zeros():
    """
    Test case for the method trailing_zeros.
    :return: None
    """
    assert com.trailing_zeros(1) == 0
    assert com.trailing_zeros(2) == 1
    assert com.trailing_zeros(3) == 0
    assert com.trailing_zeros(8) == 3
    assert com.trailing_zeros(668503069687808) == 45

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
    assert com.to_binary(0) == "0"
    assert com.to_binary(1) == "1"
    assert com.to_binary(5) == "101"
    assert com.to_binary(19373728) == "1001001111001111010100000"

    # Should only accept integers
    try:
        com.to_binary(0.25)
        assert False, "Exception expected"
    except TypeError:
        pass


def test_should_handle_big_numbers():
    """
    This test case ensures that big numbers are handled correctly if this
    is expected from the particular methods.
    :return:
    """
    # Test method next_collatz_numbers
    result = com.next_collatz_number(9**50, 3)
    assert result == 1546132562196033993109383389296863818106322566004

    result = com.next_collatz_number(result, 3)
    assert result == 773066281098016996554691694648431909053161283002

    result = com.next_collatz_number(result, 3)
    assert result == 386533140549008498277345847324215954526580641501

    # Test method next next_odd_collatz_number
    result = com.next_odd_collatz_number(9**50, 3)
    assert result == 386533140549008498277345847324215954526580641501

    # Test method collatz_sequence
    result = com.collatz_sequence(181**15, 5, 2)
    assert len(result) == 3
    assert result[0] == 7331260020097109395248329169764701
    assert result[1] == 36656300100485546976241645848823506
    assert result[2] == 18328150050242773488120822924411753

    # Test method odd_collatz_sequence
    result = com.odd_collatz_sequence(181 ** 15, 5, 1)
    assert len(result) == 2
    assert result[0] == 7331260020097109395248329169764701
    assert result[1] == 18328150050242773488120822924411753
