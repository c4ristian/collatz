"""
This module provides common methods for creating and analysing Collatz sequences.
"""
import math
import numbers
import pandas as pd


def collatz_sequence(start_value, k=3, max_iterations=-1):
    """
    This method creates a Collatz sequence for a given start value.

    The function can handle arbitrarily big integers since it uses
    native Python numbers and no third party libraries like pandas or numpy.

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


def odd_collatz_sequence(start_value, k=3, max_iterations=-1):
    """
    This method creates a Collatz sequence containing only odd numbers
    for a given start value.

    The function can handle arbitrarily big integers since it uses
    native Python numbers and no third party libraries like pandas or numpy.

    :param start_value: The integer value to start with. The value must be a
    natural number > 0. If an even number is handed over, the next odd number will be used
    as start value.
    :param k: The factor that is multiplied with odd numbers (default is 3).
    :param max_iterations: The maximum number of iterations performed
    before the method exits. Default is -1, meaning that no max number of iterations is set.
    :return: The collatz sequence as list.
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
    This method creates the next Collatz number for a given integer.

    The function can handle arbitrarily big integers since it uses
    native Python numbers and no third party libraries like pandas or numpy.

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
        # Use integer division here, in order to handle big numbers
        next_number = int_value // 2

    return int(next_number)


def next_odd_collatz_number(int_value: int, k=3):
    """
    This method creates the next odd collatz number for a given integer.

    The function can handle arbitrarily big integers since it uses
    native Python numbers and no third party libraries like pandas or numpy.

    :param int_value: The Integer value to create the next collatz number for.
    :param k: The factor that is multiplied with odd numbers (default is 3).
    :return: The next odd collatz number as integer.
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
    This method returns the components of a specific Collatz sequence as generated by
    the method _odd_collatz_components.

    :param start_value: The odd number to start with. The value must be a
    natural number > 0. If an even number is handed over, the next odd number will be used
    as start value.
    :param k: The factor that is multiplied with odd numbers (default is 3).
    :param max_iterations: The maximum number of iterations performed
    before the method exits. Default is -1, meaning that no max number of iterations is set.
    :return: A pandas data frame with the Collatz components.
    """
    result_frame = None
    odd_sequence = odd_collatz_sequence(
        start_value, k, max_iterations)

    for i, odd in enumerate(odd_sequence):
        components = _odd_collatz_components(odd, k)
        del components["vi_1"]

        current_frame = pd.DataFrame({
            "n": i + 1,
            "variable": list(components.keys()),
            "decimal": list(components.values())
        })
        if result_frame is not None:
            result_frame = result_frame.append(current_frame)
        else:
            result_frame = current_frame

    result_frame["decimal"] = result_frame["decimal"].astype('int64')
    result_frame = result_frame.reset_index(drop=True)
    result_frame = result_frame[:-2]

    return result_frame


def _odd_collatz_components(odd_number: int, k=3):
    """
    This method returns the following components of an odd Collatz
    number and a particular k factor:
    1.) vi: The odd number
    2.) kvi: The odd number multiplied with k
    3.) kvi+1: The value kvi + 1
    4.) vi_1: The next odd number
    :param odd_number: The odd number as int
    :param k: The k factor, default is three
    :return: The components as dict
    """
    v_i = odd_number
    k_vi = k * odd_number
    k_vi_1 = k_vi + 1
    vi_1 = k_vi_1 / 2**calculate_alpha(k_vi_1)
    result_dict = {
        "vi": v_i,
        "kvi": k_vi,
        "kvi+1": k_vi_1,
        "vi_1": vi_1
    }
    return result_dict


def analyse_collatz_basic_attributes(collatz_seq):
    """
    This method analyses basic attributes of a collatz sequence.

    :param collatz_seq: the sequence of collatz numbers as list.
    numbers in the sequence (default is 3),
    :return: A pandas data frame with the result of the analysis.
    """
    collatz_frame = pd.DataFrame({"collatz": collatz_seq})
    collatz_frame["odd"] = collatz_frame["collatz"] % 2
    collatz_frame["log2"] = collatz_frame["collatz"].apply(math.log2)
    collatz_frame["log2_fraction"] = collatz_frame["log2"] % 1
    collatz_frame["fraction"] = 2 ** collatz_frame["log2_fraction"]
    return collatz_frame


def calculate_alpha(int_value: int):
    """
    This method calculates the alpha (divisions by two) that is required to get from
    an even number to the next odd number in a Collatz sequence. If an odd number
    is handed over, zero will be returned.

    The function can handle arbitrarily big integers since it uses
    native Python numbers and no third party libraries like pandas or numpy.

    :param int_value: The even number as integer.
    :return: The alpha value.
    """
    assert int_value > 0, "Value > 0 expected"
    mod_result = int_value % 2

    assert mod_result in (0, 1), "Not a whole number"

    alpha = 0
    if int_value % 2 == 0:
        alpha = 1
        current_number = int_value

        while (current_number := current_number // 2) % 2 == 0:
            alpha = alpha + 1

    return alpha


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

    The function can handle arbitrarily big integers since it uses
    native Python numbers and no third party libraries like pandas or numpy.

    :param int_value: The integer to convert.
    :return: The binary representation as string.
    """
    result = bin(int_value)

    if len(result) > 2:
        result = result[2:len(result)]

    return result
