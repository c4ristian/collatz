"""
This module contains test cases for the module collatz.commons.
"""

# Imports
from math import log2
import pytest
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

    # Test if big integers are handled correctly
    result = com.collatz_sequence(181 ** 15, k=5, max_iterations=2)
    assert len(result) == 3
    assert result[0] == 7331260020097109395248329169764701
    assert result[1] == 36656300100485546976241645848823506
    assert result[2] == 18328150050242773488120822924411753

    # Should not accept numbers smaller than 1
    with pytest.raises(AssertionError):
        com.collatz_sequence(0)

    # Should only accept whole numbers
    with pytest.raises(AssertionError):
        com.next_collatz_number(0.25)


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

    # Test if big integers are handled correctly
    result = com.odd_collatz_sequence(181 ** 15, k=5, max_iterations=1)
    assert len(result) == 2
    assert result[0] == 7331260020097109395248329169764701
    assert result[1] == 18328150050242773488120822924411753

    # Should not accept numbers smaller than 1
    with pytest.raises(AssertionError):
        com.collatz_sequence(0)

    # Should only accept whole numbers
    with pytest.raises(AssertionError):
        com.next_collatz_number(0.25)


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

    # Test if big integers are handled correctly
    result = com.next_collatz_number(9 ** 50, 3)
    assert result == 1546132562196033993109383389296863818106322566004

    result = com.next_collatz_number(result, 3)
    assert result == 773066281098016996554691694648431909053161283002

    result = com.next_collatz_number(result, 3)
    assert result == 386533140549008498277345847324215954526580641501

    # Should not accept numbers smaller than 1
    with pytest.raises(AssertionError):
        com.next_collatz_number(0)

    # Should only accept whole numbers
    with pytest.raises(AssertionError):
        com.next_collatz_number(0.25)

    with pytest.raises(TypeError):
        com.next_collatz_number("abc")


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

    # Test if big integers are handled correctly
    result = com.next_odd_collatz_number(9 ** 50, 3)
    assert result == 386533140549008498277345847324215954526580641501

    # Should not accept numbers smaller than 1
    with pytest.raises(AssertionError):
        com.next_odd_collatz_number(0)

    # Should only accept whole numbers
    with pytest.raises(AssertionError):
        com.next_odd_collatz_number(0.25)

    with pytest.raises(TypeError):
        com.next_odd_collatz_number("abc")


def test_odd_collatz_sequence_components():
    """
    Test case for the method odd_collatz_sequence_components.
    :return: None
    """
    # Test different sequences
    result_frame = com.odd_collatz_sequence_components(3)
    assert list(result_frame.columns) == ["n", "variable", "decimal"]
    assert list(result_frame["n"].unique()) == [1, 2, 3]
    assert list(result_frame["variable"].unique()) == ["v_i", "kv_i", "kv_i+1"]
    assert list(result_frame["decimal"]) == [3, 9, 10, 5, 15, 16, 1]

    result_frame = com.odd_collatz_sequence_components(1, 5)
    assert list(result_frame["decimal"]) == [1, 5, 6, 3, 15, 16, 1]

    # Test if parameter max_iterations is applied
    result_frame = com.odd_collatz_sequence_components(7, k=5, max_iterations=1)
    assert list(result_frame["n"].unique()) == [1, 2]
    assert list(result_frame["decimal"]) == [7, 35, 36, 9]

    # Test if big integers are handled correctly
    result_frame = com.odd_collatz_sequence_components(
        233815871472689363774009006837127229, k=7, max_iterations=1)
    assert list(result_frame["n"].unique()) == [1, 2]
    assert list(result_frame["decimal"]) == [
        233815871472689363774009006837127229, 1636711100308825546418063047859890603,
        1636711100308825546418063047859890604, 409177775077206386604515761964972651]

    # Should not accept numbers smaller than 1
    with pytest.raises(AssertionError):
        com.odd_collatz_sequence_components(0)

    # Should only accept whole numbers
    with pytest.raises(AssertionError):
        com.odd_collatz_sequence_components(0.25)


def test_odd_collatz_components():
    """
    Test case for the method _odd_collatz_components.
    :return: None
    """
    # Test x=13 and k=3
    # pylint: disable=W0212
    comp = com._odd_collatz_components(13)
    assert comp is not None
    assert comp["v_i"] == 13
    assert comp["kv_i"] == 39
    assert comp["kv_i+1"] == 40
    assert comp["v_i+"] == 5
    # Test x=1 and k=3
    comp = com._odd_collatz_components(1, 3)
    assert comp is not None
    assert comp["v_i"] == 1
    assert comp["kv_i"] == 3
    assert comp["kv_i+1"] == 4
    assert comp["v_i+"] == 1
    # Test x=5 and k=1
    comp = com._odd_collatz_components(5, 1)
    assert comp is not None
    assert comp["v_i"] == 5
    assert comp["kv_i"] == 5
    assert comp["kv_i+1"] == 6
    assert comp["v_i+"] == 3
    # Test if big integers are handled correctly
    comp = com._odd_collatz_components(66804534706482675364002573382036351, 7)
    assert comp is not None
    assert comp["v_i"] == 66804534706482675364002573382036351
    assert comp["kv_i"] == 467631742945378727548018013674254457
    assert comp["kv_i+1"] == 467631742945378727548018013674254458
    assert comp["v_i+"] == 233815871472689363774009006837127229


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

    # Test if numbers are handled correctly
    test_sequence = [66804534706482675364002573382036351,
                     467631742945378727548018013674254458]

    analysis_frame = com.analyse_collatz_basic_attributes(test_sequence)
    assert list(analysis_frame["collatz"]) == test_sequence
    assert list(analysis_frame["odd"]) == [1, 0]
    assert list(analysis_frame["log2"].round(4)) == [115.6855, 118.4929]
    assert list(analysis_frame["log2_fraction"].round(4)) == [0.6855, 0.4929]


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

    # Test if big integers are handled correctly
    assert com.trailing_zeros(7331260020097109395248329169764701) == 0
    assert com.trailing_zeros(36656300100485546976241645848823506) == 1
    assert com.trailing_zeros(8038174778473296249349807509972772768) == 5

    # Should only accept whole numbers
    with pytest.raises(AssertionError):
        com.next_collatz_number(0.25)


def test_to_binary():
    """
    Test case for the method to_binary.
    :return: None
    """
    assert com.to_binary(0) == "0"
    assert com.to_binary(1) == "1"
    assert com.to_binary(5) == "101"
    assert com.to_binary(19373728) == "1001001111001111010100000"

    # Test if big integers are handled correctly
    assert com.to_binary(18328150050242773488120822924411753) == \
           '111000011110100101110001101101000110000110000011' \
           '000001110011101100011111011100000110101000000101' \
           '011000001101101001'

    assert int(com.to_binary(773066281098016996554691694648431909053161283002), 2) == \
           773066281098016996554691694648431909053161283002

    assert len(com.to_binary(18328150050242773488120822924411753)) == \
           int(log2(18328150050242773488120822924411753)) + 1

    # Should only accept integers
    with pytest.raises(TypeError):
        com.to_binary(0.25)


def test_multiplicative_order():
    """
    Test case for the method multiplicative_order.

    :return: None.
    """
    # Test for n = 2
    assert com.multiplicative_order(1) is None
    assert com.multiplicative_order(3) == 2
    assert com.multiplicative_order(5) == 4

    # Test max_iterations
    assert com.multiplicative_order(7, max_iterations=1) is None
    assert com.multiplicative_order(3, max_iterations=2) == 2
    assert com.multiplicative_order(181, max_iterations=10) is None
    assert com.multiplicative_order(181, max_iterations=100) is None
    assert com.multiplicative_order(181, max_iterations=1000) == 180

    # Test n=4
    assert com.multiplicative_order(7, 4) == 3

    # Should only accept integers for a
    with pytest.raises(AssertionError):
        com.multiplicative_order(0.25)
