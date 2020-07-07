"""
This python module executes different functions to set up the notebooks of
this library. The module solves for example a problem with the loading of
modules that occurs in some jupyter environments.
"""

# Imports
import sys
import pandas as pd


# Fix module loading problem
sys.path.append("..")


def set_default_pd_options():
    """
    This functions sets different default options for pandas.
    :return: None.
    """
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', 10000)
