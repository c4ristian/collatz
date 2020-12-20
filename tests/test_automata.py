"""
This module contains test cases for the module collatz.automata.
"""

# Imports
import pytest
from collatz.automata import LeadingBitsMachine


def test_leading_bits_machine():
    """
    Testcase for the class LeadingBitsMachine.

    :return: None.
    """
    # Machine starting with "101" and "111"
    machine = LeadingBitsMachine("101", "111")
    assert machine.current_state == "101"
    assert machine.previous_state == "111"
    assert str(machine) == "{previous:111, current:101}"

    next_state, lambda_i = machine.next_state()
    assert next_state == "100"
    assert lambda_i == 2
    assert machine.current_state == "100"
    assert machine.previous_state == "101"

    next_state, lambda_i = machine.next_state()
    assert next_state == "110"
    assert lambda_i == 1
    assert machine.current_state == "110"
    assert machine.previous_state == "100"

    next_state, lambda_i = machine.next_state()
    assert next_state in {"100", "101"}
    assert lambda_i == 2
    assert machine.current_state in {"100", "101"}
    assert machine.previous_state == "110"

    # Machine starting with "01" and None
    machine = LeadingBitsMachine("101")
    assert machine.current_state == "101"
    assert machine.previous_state is None
    assert str(machine) == "{previous:None, current:101}"

    next_state, lambda_i = machine.next_state()
    assert next_state in {"100", "111"}
    assert lambda_i == 1 if next_state == "111" else 2
    assert machine.current_state == next_state
    assert machine.previous_state == "101"

    # Machine with random initialization
    machine = LeadingBitsMachine()
    initial_state = machine.current_state
    assert machine.current_state in machine.valid_states
    assert machine.previous_state is None

    next_state, lambda_i = machine.next_state()
    assert next_state in machine.valid_states
    assert lambda_i in {1, 2}
    assert machine.current_state == next_state
    assert machine.previous_state == initial_state

    # Test validation
    with pytest.raises(TypeError):
        LeadingBitsMachine("ABC")

    with pytest.raises(TypeError):
        LeadingBitsMachine("101", "ABC")
