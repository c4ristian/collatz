"""
This module uses tensorflow to calculate Collatz numbers.

CAUTION: The processing of arbitrary large integers is currently not supported
due to the limitations of tensorflow.
"""

# Imports
import tensorflow as tf
import tensorflow.experimental.numpy as tnp


# Activate numpy api
tnp.experimental_enable_numpy_behavior()


# pylint: disable=C0103
# A single character for k and c is ok
def next_even_collatz_numbers(odd_numbers, k=3, c=1):
    """
    This function calculates a tensor with even Collatz numbers from
    a tensor with odd Collatz numbers.

    :param odd_numbers: A tensor with odd Collatz integers.
    :param k: The factor by which odd numbers are multiplied in the sequence (default is 3).
    :param c: The summand by which odd numbers in the sequence are increased (default is 1).
    :return: A tensor with the even Collatz integers.
    """
    return tf.add(tf.multiply(odd_numbers, k), c)


def next_odd_collatz_numbers(even_numbers):
    """
    This function calculates a tensor with odd Collatz numbers from
    a tensor with even Collatz numbers.

    :param even_numbers: A tensor with even Collatz integers.
    :return: A tensor with the odd Collatz integers.
    """
    tz = trailing_zeros(even_numbers)
    next_odd = tf.divide(even_numbers, tf.pow(2, tz))
    return tf.cast(next_odd, tf.int64)


def trailing_zeros(numbers):
    """
    This function returns a tensor with the trailing zeros
    of the binary representation of a tensor with integers.

    :param numbers: The tensor with integers.
    :return: A tensor with the trailing zeros the binary representation of the ints.
    """
    if tf.size(numbers) > 0:
        tz = tf.bitwise.bitwise_and(numbers, tf.multiply(numbers, -1))
        tz = tf.experimental.numpy.log2(tz)
    else:
        tz = numbers

    return tz
