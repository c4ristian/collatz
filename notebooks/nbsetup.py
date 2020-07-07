"""
This module provides functions for setting up the notebooks of
this library. For example, it solves a problem loading
other modules that occurs in some jupyter environments.
"""

# Imports
import sys
import pandas as pd


# Fix module loading problem
sys.path.append("..")


def set_default_pd_options():
    """
    This functions sets default options for pandas.
    :return: None.
    """
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', 10000)
