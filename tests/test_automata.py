"""
This module contains test cases for the module collatz.automata.
"""

# Imports
import pytest
from collatz.automata import LeadingBitsMachine, TrailingBitsMachine


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


def test_trailing_bits_machine():
    """
    Testcase for the class TrailingBitsMachine.

    :return: None.
    """
    # Machine starting with "001"
    machine = TrailingBitsMachine("001")
    assert machine.current_state == "001"
    assert machine.previous_state is None
    assert str(machine) == "{previous:None, current:001}"

    next_state, omega_i = machine.next_state()
    assert next_state in {"001", "011", "101", "111"}
    assert -1 <= omega_i <= 0
    assert machine.current_state == next_state
    assert machine.previous_state == "001"

    # Machine starting with "011"
    machine = TrailingBitsMachine("011")
    assert machine.current_state == "011"
    assert machine.previous_state is None
    assert str(machine) == "{previous:None, current:011}"

    next_state, omega_i = machine.next_state()
    assert next_state in {"001", "101"}
    assert 0 <= omega_i <= 1
    assert machine.current_state == next_state
    assert machine.previous_state == "011"

    next_state, omega_i = machine.next_state()
    assert next_state in {"001", "011", "101", "111"}
    assert -3 <= omega_i <= 0

    # Machine starting with "101"
    machine = TrailingBitsMachine("101")
    assert machine.current_state == "101"
    assert machine.previous_state is None
    assert str(machine) == "{previous:None, current:101}"

    next_state, omega_i = machine.next_state()
    assert next_state in {"001", "011", "101", "111"}
    assert omega_i <= -1
    assert machine.current_state == next_state
    assert machine.previous_state == "101"

    # Machine starting with "101"
    machine = TrailingBitsMachine("111")
    assert machine.current_state == "111"
    assert machine.previous_state is None
    assert str(machine) == "{previous:None, current:111}"

    next_state, omega_i = machine.next_state(lambda_i=1)
    assert next_state in {"011", "111"}
    assert omega_i == 0
    assert machine.current_state == next_state
    assert machine.previous_state == "111"

    machine = TrailingBitsMachine("111")
    next_state, omega_i = machine.next_state(lambda_i=2)
    assert next_state in {"011", "111"}
    assert omega_i == 1

    # Test validation
    with pytest.raises(TypeError):
        LeadingBitsMachine("ABC")

    with pytest.raises(TypeError):
        LeadingBitsMachine("101", "ABC")
