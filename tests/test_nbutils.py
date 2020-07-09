"""
This module contains test cases for the module collatz.commons.
"""

# Imports
import pandas as pd
from notebooks import nbutils


def test_set_default_pd_options():
    """
    Test case for the method set_default_pd_options.
    :return: None
    """
    nbutils.set_default_pd_options()
    assert not pd.get_option('display.expand_frame_repr')
    assert pd.get_option('display.max_rows') == 10000


def test_rnd_int():
    """
    Test case for the method rnd_int.
    :return: None
    """
    assert nbutils.rnd_int(1) == 1
    assert nbutils.rnd_int(2) <= 2

    # Should not accept numbers < 1
    try:
        nbutils.rnd_int(0)
        assert False, "Exception expected"
    except ValueError:
        pass

    # Test odds only
    assert nbutils.rnd_int(1, odds_only=True) == 1
    assert nbutils.rnd_int(3, odds_only=True) in [1, 3]

    assert nbutils.rnd_int(2, odds_only=True) == 1

    # Should not accept numbers < 1
    try:
        nbutils.rnd_int(-1, odds_only=True)
        assert False, "Exception expected"
    except ValueError:
        pass
