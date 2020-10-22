"""
This module contains test cases for the module collatz.generator. Some of the tests are not
completely deterministic and might fail in very rare cases, even though the probability is
very low.
"""

# Imports
from collatz import generator


def test_should_generate_collatz_sequence_correctly():
    """
    Test case for the method generate_collatz_sequence.
    :return: None
    """
    # Test simple sequence
    result = generator.generate_collatz_sequence(start_value=1)

    assert result is not None
    assert len(result) == 4
    assert list(result["collatz_index"]) == [0, 1, 2, 3]
    assert list(result["collatz"]) == [1, 4, 2, 1]
    assert set(result["k_factor"]) == {3}
    assert list(result["next_collatz"]) == [4, 2, 1, 4]
    assert list(result["next_odd"]) == [1, 1, 1, 1]

    assert result["collatz"].dtype == 'int64'
    assert result["next_odd"].dtype == 'int64'
    assert result["next_collatz"].dtype == 'int64'

    # Test with eternal sequence
    result = generator.generate_collatz_sequence(start_value=1, k=2, max_iterations=3)

    assert result is not None
    assert len(result) == 4
    assert set(result["k_factor"]) == {2}
    assert list(result["collatz"]) == [1, 3, 7, 15]
    assert list(result["next_collatz"]) == [3, 7, 15, 31]
    assert list(result["next_odd"]) == [3, 7, 15, 31]

    # Test default value of max_iterations
    result = generator.generate_collatz_sequence(start_value=1, k=2)
    assert len(result) == 101

    # Test with k=5
    result = generator.generate_collatz_sequence(start_value=13, k=5, max_iterations=500)
    result = result[result["odd"] == 1]
    assert result is not None
    assert len(result) == 4
    assert list(result["collatz"]) == [13, 33, 83, 13]
    assert list(result["next_odd"]) == [33, 83, 13, 33]

    # Test if big integers are handled correctly
    result = generator.generate_collatz_sequence(
        start_value=9**50, k=9, max_iterations=2)

    assert result is not None
    assert len(result) == 3
    assert result["collatz"].dtype == 'object'
    assert result["next_odd"].dtype == 'object'
    assert result["next_collatz"].dtype == 'object'

    assert list(result["collatz"]) == [
        9**50, 9**51+1, 2319198843294050989664075083945295727159483849005]

    assert list(result["next_collatz"]) == [
        9**51+1, 2319198843294050989664075083945295727159483849005,
        20872789589646458906976675755507661544435354641046
    ]

    assert list(result["next_odd"]) == [
        2319198843294050989664075083945295727159483849005,
        2319198843294050989664075083945295727159483849005,
        10436394794823229453488337877753830772217677320523
    ]


def test_should_generate_odd_collatz_sequence_correctly():
    """
    Test case for the method generate_odd_collatz_sequence.
    :return: None
    """
    # Test simple sequence
    result = generator.generate_odd_collatz_sequence(start_value=1)

    assert result is not None
    assert len(result) == 2
    assert list(result["odd_index"]) == [0, 1]
    assert list(result["collatz"]) == [1, 1]
    assert set(result["k_factor"]) == {3}
    assert list(result["next_collatz"]) == [4, 4]
    assert list(result["next_odd"]) == [1, 1]

    assert result["collatz"].dtype == 'int64'
    assert result["next_odd"].dtype == 'int64'
    assert result["next_collatz"].dtype == 'int64'

    # Test with eternal sequence
    result = generator.generate_odd_collatz_sequence(start_value=1, k=2, max_iterations=3)

    assert result is not None
    assert len(result) == 4
    assert set(result["k_factor"]) == {2}
    assert list(result["collatz"]) == [1, 3, 7, 15]
    assert list(result["next_collatz"]) == [3, 7, 15, 31]
    assert list(result["next_odd"]) == [3, 7, 15, 31]

    # Test default value of max_iterations
    result = generator.generate_odd_collatz_sequence(start_value=1, k=2)
    assert len(result) == 101

    # Test with k=5
    result = generator.generate_odd_collatz_sequence(start_value=13, k=5, max_iterations=500)
    assert result is not None
    assert len(result) == 4
    assert list(result["collatz"]) == [13, 33, 83, 13]
    assert list(result["next_odd"]) == [33, 83, 13, 33]

    # Test if big integers are handled correctly
    result = generator.generate_odd_collatz_sequence(
        start_value=9 ** 50, k=9, max_iterations=1)

    assert result["collatz"].dtype == 'object'
    assert result["next_odd"].dtype == 'object'
    assert result["next_collatz"].dtype == 'object'

    assert list(result["collatz"]) == [
        9 ** 50, 2319198843294050989664075083945295727159483849005]

    assert list(result["next_collatz"]) == [
        9**51+1, 20872789589646458906976675755507661544435354641046]

    assert list(result["next_odd"]) == [
        2319198843294050989664075083945295727159483849005,
        10436394794823229453488337877753830772217677320523]
