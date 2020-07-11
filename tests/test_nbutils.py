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


def test_to_binary():
    """
    Test case for the method to_binary.
    :return: None
    """
    assert nbutils.to_binary(1) == "1"
    assert nbutils.to_binary(5) == "101"
    assert nbutils.to_binary("256") == "100000000"

    assert nbutils.to_binary("018328150050242773488120822924411753") == \
           '111000011110100101110001101101000110000110000011' \
           '000001110011101100011111011100000110101000000101' \
           '011000001101101001'

    # Should only accept integers
    with pytest.raises(TypeError):
        nbutils.to_binary(0.25)

    with pytest.raises(ValueError):
        nbutils.to_binary("0.25")

    with pytest.raises(ValueError):
        nbutils.to_binary("abc")
