"""
This module contains test cases for the module collatz.generator. Some of the tests are not
completely deterministic and might fail in very rare cases, even though the probability is
very low.
"""

# Imports
from collatz import generator


def test_should_generate_collatz_sequence_correctly():
    """
    This method tests that single collatz sequences are generated correctly.
    :return: None
    """
    # Test simple sequence
    result = generator.generate_collatz_sequence(start_value=1)

    assert result is not None, "result should not be None"
    assert len(result) == 4, "expected different length"
    assert list(result["collatz_index"]) == [0, 1, 2, 3], "expected different index"
    assert list(result["collatz"]) == [1, 4, 2, 1], "expected different sequence"
    assert set(result["k_factor"]) == {3}, "expected different k factor"
    assert list(result["next_collatz"]) == [4, 2, 1, 4], "expected different sequence"
    assert list(result["next_odd"]) == [1, 1, 1, 1], "expected different sequence"

    # Test with eternal sequence
    result = generator.generate_collatz_sequence(start_value=1, k=2, max_iterations=3)

    assert result is not None, "result should not be None"
    assert len(result) == 4, "expected different length"
    assert set(result["k_factor"]) == {2}, "expected different k factor"
    assert list(result["collatz"]) == [1, 3, 7, 15], "expected different sequence"
    assert list(result["next_collatz"]) == [3, 7, 15, 31], "expected different sequence"
    assert list(result["next_odd"]) == [3, 7, 15, 31], "expected different sequence"

    # Test with k=5
    result = generator.generate_collatz_sequence(start_value=13, k=5, max_iterations=500)
    result = result[result["odd"] == 1]
    assert result is not None, "result should not be None"
    assert len(result) == 4, "expected different length"
    assert list(result["collatz"]) == [13, 33, 83, 13], "expected different sequence"
    assert list(result["next_odd"]) == [33, 83, 13, 33], "expected different sequence"


def test_should_generate_random_sequence_correctly():
    """
    This method tests that single random collatz sequences is generated correctly.
    :return: None
    """
    # Test simple sequence
    result = generator.generate_random_sequence(max_start_value=1, k_factors=[3])
    assert list(result["collatz"]) == [1, 4, 2, 1], "expected different sequence"
    assert set(result["k_factor"]) == {3}, "expected different k factor"

    # Test with eternal sequence
    result = generator.generate_random_sequence(
        max_start_value=1, k_factors=[2], max_iterations=3)

    assert set(result["k_factor"]) == {2}, "expected different k factor"
    assert list(result["collatz"]) == [1, 3, 7, 15], "expected different sequence"

    # Test with different k factors and different starting values
    result = generator.generate_random_sequence(
        max_start_value=5, k_factors=[2, 3], max_iterations=5)

    assert len(result) <= 6, "expected different length"
    assert 1 <= result["collatz"][0] <= 5, "expected different sequence"

    k_factor = set(result["k_factor"]).pop()
    assert k_factor in {2, 3}, "expected different k factor"


def test_should_generate_random_sequences_correctly():
    """
    This method tests that multiple collatz sequences are generated correctly.
    :return: None
    """
    # Test simple sequence
    result = generator.generate_random_sequences(n=2, max_start_value=1, k_factors=[3])

    assert result is not None, "result should not be None"
    assert len(result) == 8, "expected different length"
    assert set(result["k_factor"]) == {3}, "expected different k factor"
    assert set(result["sequence_index"]) == {0, 1}, "expected different k factor"

    first_frame = result[result["sequence_index"] == 0]
    second_frame = result[result["sequence_index"] == 1]

    assert list(first_frame["collatz"]) == [1, 4, 2, 1], "expected different sequence"
    assert list(second_frame["collatz"]) == [1, 4, 2, 1], "expected different sequence"

    # Test more complex sequences
    result = generator.generate_random_sequences(
        n=100, max_start_value=5, k_factors=[3, 5], max_iterations=5)

    assert result is not None, "result should not be None"
    assert len(result) > 1, "expected different length"
    assert set(result["sequence_index"]) == set(range(0, 100)), "expected different k factor"

    # This test is not completely deterministic it might fail in rare cases, even
    # though the probability is very low
    assert set(result["k_factor"]) == {3, 5}, "expected different k factor"
