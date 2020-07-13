"""
This module provides utility functions for the notebooks of
the Collatz library.
"""

# Imports
import sys
import random as rnd
import pandas as pd

# Fix possible import problems
sys.path.append("..")


def set_default_pd_options():
    """
    This functions sets default options for pandas.
    :return: None.
    """
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', 10000)


def rnd_int(max_value: int, odds_only=False):
    """
    This function returns a random integer value between 1 and a given maximum value.
    :param max_value: The maximum value as int.
    :param odds_only: If this parameter is True only odd ints
    are considered (default is False).
    :return: The random integer value.
    """
    random_int = rnd.randint(1, max_value)

    if odds_only and random_int % 2 == 0:
        random_int = random_int + 1

        if random_int > max_value:
            random_int = random_int - 2

    return random_int
