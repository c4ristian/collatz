"""
This module contains test cases for the module notebooks.nbutils.
"""

# Imports
import pytest
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
    with pytest.raises(ValueError):
        nbutils.rnd_int(0)

    # Test odds only
    assert nbutils.rnd_int(1, odds_only=True) == 1
    assert nbutils.rnd_int(3, odds_only=True) in [1, 3]

    assert nbutils.rnd_int(2, odds_only=True) == 1

    # Should not accept numbers < 1
    with pytest.raises(ValueError):
        nbutils.rnd_int(-1, odds_only=True)


def test_swap_column_names():
    """
    Test case for the method swap_column_names.
    :return: None.
    """
    # Test happy path
    list1 = [1, 2]
    list2 = [2, 1]

    data_frame = pd.DataFrame({
        "list1": list1,
        "list2": list2
    })

    nbutils.swap_column_names(("list1", "list2"), data_frame)
    assert list(data_frame["list1"]) == list2
    assert list(data_frame["list2"]) == list1

    # Should only accept tuples for column names
    with pytest.raises(AssertionError):
        nbutils.swap_column_names(1, pd.DataFrame)

    # Should only accept data frames
    with pytest.raises(AssertionError):
        nbutils.swap_column_names(("a", "b"), 1)
