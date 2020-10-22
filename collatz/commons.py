"""
This module provides common methods for creating and analysing Collatz sequences. All
functions are optimised for handling arbitrary big integers. The precision of
calculated float values depends on the precision of the underlying data type in
Python and pandas.
"""
import math
import numbers
import pandas as pd


def collatz_sequence(start_value, k=3, max_iterations=-1):
    """
    This method creates a Collatz sequence for a given start value.

    :param start_value: The int value to start with. The value must be a natural number > 0.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param max_iterations: The maximum number of iterations performed
        before the method exits. Default is -1, which means that the number of
        iterations is not limited.
    :return: The Collatz sequence as list.
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


def odd_collatz_sequence(start_value, k=3, max_iterations=-1):
    """
    This method creates a Collatz sequence containing only odd numbers
    for a given start value.

    :param start_value: The int value to start with. The value must be a
        natural number > 0. If an even number is handed over, the next odd number will be used
        as start value.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param max_iterations: The maximum number of iterations performed
        before the method exits. Default is -1, which means that the number of
        iterations is not limited.
    :return: The Collatz sequence as list.
    """
    # Possibly transform start value
    if start_value % 2 == 0:
        start_value = next_odd_collatz_number(start_value, k)

    # Create a result list, including the start value
    result_list = [start_value]

    # Calculate next odd collatz number
    current_odd = next_odd_collatz_number(start_value, k)

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
        current_odd = next_odd_collatz_number(current_odd, k)

    # Append the final value
    result_list.append(current_odd)

    return result_list


def next_collatz_number(int_value, k=3):
    """
    This method calculates the next Collatz number for a given int value.

    :param int_value: The int value to calculate the next Collatz number for. The value
        must be a natural number > 0.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :return: The next Collatz number as int.
    """
    assert int_value > 0, "Value > 0 expected"

    mod_result = int_value % 2
    assert mod_result in (0, 1), "Not a natural number"

    # odd number
    if mod_result == 1:
        next_number = int_value * k + 1
    # even number
    else:
        # Use integer division here, in order to handle big numbers
        next_number = int_value // 2

    return int(next_number)


def next_odd_collatz_number(int_value: int, k=3):
    """
    This method calculates the next odd Collatz number for a given int value.

    :param int_value: The int value to calculate the next Collatz number for.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :return: The next odd Collatz number as int.
    """
    assert int_value > 0, "Value > 0 expected"
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
        next_odd = int_value

        while (next_odd := next_collatz_number(next_odd, k)) % 2 == 0:
            continue

    return int(next_odd)


def odd_collatz_sequence_components(
        start_value: int, k=3, max_iterations=100):
    """
    This method returns the components of a specific Collatz sequence.

    :param start_value: The odd number to start with. The value must be a
        natural number > 0. If an even number is handed over, the next odd number will be used
        as start value.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param max_iterations: The maximum number of iterations performed
        before the method exits. Default is -1, which means that the number of
        iterations is not limited.
    :return: A pandas data frame with the Collatz components.
    """
    result_frame = None
    odd_sequence = odd_collatz_sequence(
        start_value, k, max_iterations)

    for i, odd in enumerate(odd_sequence):
        components = _odd_collatz_components(odd, k)
        del components["v_i+"]

        current_frame = pd.DataFrame({
            "n": i + 1,
            "variable": list(components.keys()),
            "decimal": list(components.values())
        })
        if result_frame is not None:
            result_frame = result_frame.append(current_frame)
        else:
            result_frame = current_frame

    result_frame["decimal"] = result_frame["decimal"]
    result_frame = result_frame.reset_index(drop=True)
    result_frame = result_frame[:-2]

    return result_frame


def _odd_collatz_components(odd_number: int, k=3):
    """
    This method returns the following components of an odd Collatz
    number and a particular k factor:
    1.) v_i: The odd number
    2.) kv_i: The odd number multiplied with k
    3.) kv_i+1: The value kvi + 1
    4.) v_i+: The next odd number

    :param odd_number: The odd number as int
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :return: The components as dict
    """
    v_i = odd_number
    k_vi = k * odd_number
    k_vi_1 = k_vi + 1
    vi_1 = k_vi_1 // 2**trailing_zeros(k_vi_1)
    result_dict = {
        "v_i": v_i,
        "kv_i": k_vi,
        "kv_i+1": k_vi_1,
        "v_i+": vi_1
    }
    return result_dict


def analyse_collatz_basic_attributes(collatz_seq: list):
    """
    This method analyses basic attributes of a Collatz sequence.

    :param collatz_seq: the sequence of Collatz numbers as list.
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
    This method returns the trailing zeros of the binary representation of an integer.

    :param int_value: The int value.
    :return: The trailing zeros as int.
    """
    assert isinstance(int_value, numbers.Integral), "Integer value expected"
    result = int(math.log2(int_value & int_value * -1))
    return result


def to_binary(int_value: int):
    """
    This method converts an int to its binary representation.

    :param int_value: The int value to convert.
    :return: The binary representation as str.
    """
    result = bin(int_value)

    if len(result) > 2:
        result = result[2:len(result)]

    return result


# pylint: disable=C0103
# A single character for a and n is ok, since this is compliant with
# the wiki-documentation
def multiplicative_order(a: int, n=2, max_iterations=10):
    """
    This method returns the multiplicative order of an integer *a modulo n*.
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
