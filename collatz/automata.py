"""
This module provides automata that model certain aspects of the Collatz problem.
"""

# Imports
import random


class LeadingBitsMachine:
    """
    This finite state machine models the transitions between the leading three
    bits of odd Collatz numbers. The machine is a nondeterministic transducer whose states
    represent the bits. As input, the automaton receives the previous state
    or *None* if no previous state exists. As output the machine returns
    the growth of the binary number (lambda) as described in
    (https://doi.org/10.18052/www.scipress.com/IJPMS.21.1)

    The machine only works for the Collatz problem in its original form *3v+1*.
    """
    def __init__(self, current_state=None, previous_state=None):
        """
        Creates a new LeadingBitsMachine.

        :param current_state: The current state (leading bits of the
            current odd Collatz number as str) or None. If None is handed over, the
            current state is chosen randomly.
        :param previous_state: The previous state (leading bits of the
            previous odd Collatz number as str) or None.
        """
        self.valid_states = {"100", "101", "110", "111"}
        self._validate_state(current_state)
        self._validate_state(previous_state)

        if current_state is None:
            self.current_state = self._random_state(self.valid_states)
        else:
            self.current_state = current_state
        self.previous_state = previous_state

    def _validate_state(self, state):
        """
        This method validates a certain state. A state is considered valid
        if it is either None or is in the set *self.valid_states*. If a state is not valid
        a TypeError is raised.

        :param state: The state to validate.
        :return: None.
        """
        valid = state is None or state in self.valid_states
        if not valid:
            raise TypeError("Illegal state: " + state)

    @staticmethod
    def _random_state(states):
        """
        This function returns a randomly chosen item of a sequence of states.

        :param states: The sequence of states.
        :return: The randomly chosen state.
        """
        return random.sample(states, k=1)[0]

    def next_state(self):
        """
        This method moves the machine to the next state based on the current state
        and the previous state, which serves as input.

        :return: The next state and the binary growth lambda as output.
        """
        next_state = None
        lambda_i = None

        if self.current_state == "100":
            lambda_i = 1
            if self.previous_state == "101":
                next_state = "110"
            else:
                next_state = self._random_state({"110", "111"})
        elif self.current_state == "101":
            if self.previous_state == "111":
                next_state = "100"
                lambda_i = 2
            elif self.previous_state == "110":
                next_state = "111"
                lambda_i = 1
            else:
                next_state = self._random_state({"100", "111"})
                lambda_i = 1 if next_state == "111" else 2
        elif self.current_state == "110":
            next_state = self._random_state({"100", "101"})
            lambda_i = 2
        elif self.current_state == "111":
            next_state = "101"
            lambda_i = 2

        self.previous_state = self.current_state
        self.current_state = next_state
        return next_state, lambda_i

    def __str__(self):
        return "{previous:" + str(self.previous_state) + ", "\
               "current:" + str(self.current_state) + "}"
