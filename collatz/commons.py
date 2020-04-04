"""
This module provides common methods for creating and analysing Collatz sequences.
"""
import math
import numbers
import pandas as pd


def collatz_sequence(start_value, k=3, max_iterations=-1):
    """
    This method creates a Collatz sequence for a given start value.

    :param start_value: The integer value to start with.
    The value must be a natural number > 0.
    :param k: The factor that is multiplied with odd numbers (default is 3).
    :param max_iterations: The maximum number of iterations performed
    before the method exits. Default is -1, meaning that no max number of iterations is set.
    :return: The collatz sequence as list.
    """
    # Create a result list, including the start value
    result_list = [start_value]

    # Calculate next collatz number
    current_collatz = next_collatz_number(start_value, k)

    # Create the sequence and stop only if 1 or a cycle occur
    iteration_counter = 1

    while current_collatz != 1 and current_collatz not in result_list:
        # Break when the max number of iterations is set
        if -1 < max_iterations <= iteration_counter:
            break

        # Increase iteration counter
        iteration_counter += 1

        # Create the next collatz number
        result_list.append(current_collatz)
        current_collatz = next_collatz_number(current_collatz, k)

    # Append the final value
    result_list.append(current_collatz)

    return result_list


def next_collatz_number(int_value, k=3):
    """
    This method creates the next Collatz number for a given integer.

    :param int_value: The integer value to create the next Collatz number for. The value
    must be a natural number > 0.
    :param k: The factor that is multiplied with odd numbers (default is 3).
    :return: The next collatz number as Integer.
    """
    assert int_value > 0, "Value > 0 expected"

    mod_result = int_value % 2
    assert mod_result in (0, 1), "Not a natural number"

    # odd number
    if mod_result == 1:
        next_number = int_value * k + 1
    # even number
    else:
        next_number = int_value / 2

    return int(next_number)


def next_odd_collatz_number(int_value, k=3):
    """
    This method creates the next odd collatz number for a given integer.

    :param int_value: The Integer value to create the next collatz number for.
    :param k: The factor that is multiplied with odd numbers (default is 3).
    :return: The next odd collatz number as integer.
    """
    assert int_value > 0, "Value > 0 expected"

    next_odd = None
    mod_result = int_value % 2

    assert mod_result in (0, 1), "Not a whole number"

    # odd number
    if mod_result == 1:
        next_element = next_collatz_number(int_value, k)

        if next_element % 2 == 1:
            next_odd = next_element
        else:
            next_odd = next_odd_collatz_number(next_element, k)
    # even number
    else:
        next_odd = int_value * 2 ** -trailing_zeros(int_value)

    return int(next_odd)


def analyse_collatz_basic_attributes(collatz_seq):
    """
    This method analyses basic attributes of a collatz sequence.

    :param collatz_seq: the sequence of collatz numbers as list.
    numbers in the sequence (default is 3),
    :return: A data frame with the result of the analysis.
    """
    collatz_frame = pd.DataFrame({"collatz": collatz_seq})
    collatz_frame["odd"] = collatz_frame["collatz"] % 2
    collatz_frame["log2"] = collatz_frame["collatz"].apply(math.log2)
    collatz_frame["log2_fraction"] = collatz_frame["log2"] % 1
    collatz_frame["fraction"] = 2 ** collatz_frame["log2_fraction"]
    return collatz_frame


def analyse_collatz_binary_attributes(collatz_seq):
    """
    This method analyses basic attributes of a collatz sequence.
    :param collatz_seq: the sequence of collatz numbers as list
    :return: a data frame with the result of the analysis
    """
    collatz_frame = pd.DataFrame({"collatz": collatz_seq})
    collatz_frame["bin_tz"] = collatz_frame["collatz"].apply(trailing_zeros)
    collatz_frame["bin_str"] = collatz_frame["collatz"].apply(to_binary)
    collatz_frame["bin_len"] = collatz_frame["bin_str"].apply(len)
    collatz_frame = collatz_frame[["collatz", "bin_str", "bin_len", "bin_tz"]]
    return collatz_frame


def trailing_zeros(int_value):
    """
    This method returns the trailing zeros of the binary representation of an integer.

    :param int_value: The int value.
    :return: The trailing zeros.
    """
    assert isinstance(int_value, numbers.Integral), "Integer value expected"
    result = math.log2(int_value & int_value * -1)
    return result


def to_binary(int_value):
    """
    This method converts an integer to its binary representation.

    :param int_value: The integer to convert.
    :return: The binary representation as string.
    """
    result = bin(int_value)

    if len(result) > 2:
        result = result[2:len(result)]

    return result
