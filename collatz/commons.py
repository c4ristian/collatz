"""
This module provides common methods for creating and analysing Collatz sequences. All
functions are optimised for handling arbitrary big integers. The precision of
calculated float values depends on the precision of the underlying data type in
Python and pandas. The module provides functions for Collatz sequences both in the
original form *3v+1* as well as in the generalised variant *kv+c*.
"""
import math
import numbers
from collections import deque
import pandas as pd


# pylint: disable=C0103
# A single character for k and c is ok
def collatz_sequence(start_value, k=3, c=1, max_iterations=-1):
    """
    This method creates a Collatz sequence for a given start value.

    :param start_value: The int value to start with. The value must be a natural number > 0.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :param max_iterations: The maximum number of iterations performed
        before the method exits. Default is -1, which means that the number of
        iterations is not limited.
    :return: The Collatz sequence as list.
    """
    # Create a result list, including the start value
    result_list = [start_value]

    # Calculate next collatz number
    current_collatz = next_collatz_number(start_value, k, c)

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
        current_collatz = next_collatz_number(current_collatz, k, c)

    # Append the final value
    result_list.append(current_collatz)

    return result_list


def odd_collatz_sequence(start_value, k=3, c=1, max_iterations=-1):
    """
    This method creates a Collatz sequence containing only odd numbers
    for a given start value.

    :param start_value: The int value to start with. The value must be a
        natural number > 0. If an even number is handed over, the next odd number will be used
        as start value.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :param max_iterations: The maximum number of iterations performed
        before the method exits. Default is -1, which means that the number of
        iterations is not limited.
    :return: The Collatz sequence as list.
    """
    # Possibly transform start value
    if start_value % 2 == 0:
        start_value = next_odd_collatz_number(start_value, k, c)

    # Create a result list, including the start value
    result_list = [start_value]

    # Calculate next odd collatz number
    current_odd = next_odd_collatz_number(start_value, k, c)

    # Create the sequence and stop only if 1 or a cycle occur
    iteration_counter = 1

    while current_odd != 1 and current_odd not in result_list:
        # Break when the max number of iterations is set
        if -1 < max_iterations <= iteration_counter:
            break

        # Increase iteration counter
        iteration_counter += 1

        # Create the next collatz number
        result_list.append(current_odd)
        current_odd = next_odd_collatz_number(current_odd, k, c)

    # Append the final value
    result_list.append(current_odd)

    return result_list


def next_collatz_number(int_value, k=3, c=1):
    """
    This method calculates the next Collatz number for a given int value.

    :param int_value: The int value to calculate the next Collatz number for. The value
        must be a natural number > 0.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :return: The next Collatz number as int.
    """
    assert int_value > 0, "Value > 0 expected"

    mod_result = int_value % 2
    assert mod_result in (0, 1), "Not a natural number"

    # odd number
    if mod_result == 1:
        next_number = int_value * k + c
    # even number
    else:
        # Use integer division here, in order to handle big numbers
        next_number = int_value // 2

    return int(next_number)


def next_odd_collatz_number(int_value: int, k=3, c=1):
    """
    This method calculates the next odd Collatz number for a given int value.

    :param int_value: The int value to calculate the next Collatz number for.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :return: The next odd Collatz number as int.
    """
    assert int_value > 0, "Value > 0 expected"
    mod_result = int_value % 2

    assert mod_result in (0, 1), "Not a whole number"

    # odd number
    if mod_result == 1:
        next_element = next_collatz_number(int_value, k, c)

        if next_element % 2 == 1:
            next_odd = next_element
        else:
            next_odd = next_odd_collatz_number(next_element, k, c)
    # even number
    else:
        next_odd = int_value

        while (next_odd := next_collatz_number(next_odd, k, c)) % 2 == 0:
            continue

    return int(next_odd)


def odd_collatz_sequence_components(start_value: int, k=3, c=1, max_iterations=100):
    """
    This method returns the components of a specific Collatz sequence.

    :param start_value: The odd number to start with. The value must be a
        natural number > 0. If an even number is handed over, the next odd number will be used
        as start value.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :param max_iterations: The maximum number of iterations performed
        before the method exits. Default is -1, which means that the number of
        iterations is not limited.
    :return: A pandas data frame with the Collatz components.
    """
    result_frame = None
    odd_sequence = odd_collatz_sequence(start_value, k, c, max_iterations)

    for i, odd in enumerate(odd_sequence):
        components = _odd_collatz_components(odd, k, c)
        del components["v_i+"]

        current_frame = pd.DataFrame({
            "n": i + 1,
            "variable": list(components.keys()),
            "decimal": list(components.values())
        })
        if result_frame is not None:
            result_frame = pd.concat([result_frame, current_frame])
        else:
            result_frame = current_frame

    result_frame["decimal"] = result_frame["decimal"]
    result_frame = result_frame.reset_index(drop=True)
    result_frame = result_frame[:-2]

    return result_frame


def _odd_collatz_components(odd_number: int, k=3, c=1):
    """
    This method returns the following components of an odd Collatz
    number and a particular k factor:
    1.) v_i: The odd number
    2.) kv_i: The odd number multiplied with k
    3.) kv_i+c: The value kvi + c
    4.) v_i+: The next odd number

    :param odd_number: The odd number as int.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :return: The components as dict.
    """
    v_i = odd_number
    k_vi = k * odd_number
    k_vi_c = k_vi + c
    vi_1 = k_vi_c // 2**trailing_zeros(k_vi_c)
    result_dict = {
        "v_i": v_i,
        "kv_i": k_vi,
        "kv_i+c": k_vi_c,
        "v_i+": vi_1
    }
    return result_dict


def analyse_collatz_basic_attributes(collatz_seq: list):
    """
    This method analyses basic attributes of a Collatz sequence.

    :param collatz_seq: The sequence of Collatz numbers as list.
    :return: A pandas data frame with the results of the analysis.
    """
    collatz_frame = pd.DataFrame({"collatz": collatz_seq})
    collatz_frame["odd"] = collatz_frame["collatz"] % 2
    collatz_frame["log2"] = collatz_frame["collatz"].apply(math.log2)
    collatz_frame["log2_fraction"] = collatz_frame["log2"] % 1
    collatz_frame["fraction"] = 2 ** collatz_frame["log2_fraction"]
    return collatz_frame


def trailing_zeros(int_value: int):
    """
    This method returns the trailing zeros of the binary representation of an int value.

    :param int_value: The int value.
    :return: The trailing zeros as int.
    """
    if not isinstance(int_value, numbers.Integral):
        raise TypeError("Integer value expected")

    result = int(math.log2(int_value & int_value * -1))
    return result


def trailing_ones(int_value: int):
    """
    This method returns the trailing ones of the binary representation of an int value.

    :param int_value: The int value.
    :return: The trailing ones as int.
    """
    return trailing_ones_str(to_binary(int_value))


def trailing_ones_str(bin_str: str):
    """
    This method returns the trailing ones of a binary number formatted as string.

    :param bin_str: The binary number as str.
    :return: The trailing ones as int.
    """
    # Only strings are allowed
    if not isinstance(bin_str, str):
        raise TypeError("String value expected")

    # Right trim
    bin_str = bin_str.rstrip()

    # Remove possible leading "b" from binary str
    if len(bin_str) > 0 and bin_str[-1] == "b":
        bin_str = bin_str[:-1]

    # Count trailing ones
    ones = 0
    for index in range(len(bin_str)):
        c = bin_str[len(bin_str) - index - 1]

        if c == "1":
            ones += 1
        else:
            break

    return ones


def to_binary(int_value: int):
    """
    This method converts an int to its binary representation.

    :param int_value: The int value to convert.
    :return: The binary representation as str.
    """
    # The implementation does not build on to_numeral
    # because the native Python conversion is faster
    result = bin(int_value)

    if len(result) > 2:
        result = result[2:len(result)]

    return result


def to_numeral(x: int, base: int, sep=None) -> str:
    """
    This function converts an int into its representation in a specific numeral system.

    Only the letters '0-9' are supported. For numeral systems with a base greater than 10,
    a separator must be specified. The minimum supported base is 2.

    :param x: The int to convert.
    :param base: The base of the numeral system (e.g. 3 for ternary), minimum is 2.
    :param sep: The separator to be used, default is None.
    :return: The representation in the numeral system as str.
    """
    if base > 10 and sep is None:
        raise AttributeError(
            "For base>10 a separator is required!")

    result_list = _to_numeral_sequence(x, base)

    result = "" if sep is None else sep
    result = result.join(str(n) for n in result_list)
    return result


def _to_numeral_sequence(x: int, base: int) -> deque:
    """
    This function converts an int into its representation in a specific numeral system.

    Only the letters '0-9' are supported. The result is returned as a deque.

    :param x: The int to convert.
    :param base: The base of the numeral system (e.g. 3 for ternary), minimum is 2.
    :return: The representation in the numeral system as deque.
    """
    if not isinstance(x, numbers.Integral):
        raise TypeError("Integer value expected")
    if base <= 1:
        raise AttributeError(
            "Parameter base must be > 1")

    remainder = x % base
    quotient = x // base
    digits = deque([remainder])

    while quotient:
        remainder = quotient % base
        quotient = quotient // base
        digits.appendleft(remainder)

    return digits


def multiplicative_order(a: int, n=2, max_iterations=10):
    """
    This method returns the multiplicative order of an int *a modulo n*.
    For a description of the algorithm see https://en.wikipedia.org/wiki/Multiplicative_order.

    :param a: An int whose multiplicative order is to be defined.
    :param n: The parameter n which is used for the modulo operation.
    :param max_iterations: The maximum number of iterations to be performed. If no result
        has been determined after this number of iterations, None is returned.
    :return: The multiplicative order or None if no result has been found.
    """
    assert isinstance(a, numbers.Integral), "Integer value expected"

    order = None

    for e in range(1, max_iterations + 1):
        if n**e % a == 1:
            order = e
            break

    return order
