"""
This module provides automata that model certain aspects of the Collatz problem.
"""

# Imports
from abc import ABC, abstractmethod
import random


class AbstractStateMachine(ABC):
    """
    This abstract base class represents a finite state machine that models Collatz numbers.
    Every state machine derived from this class has a current state and a previous state, which
    is allowed to be *None*. The machine can be moved to the next state by calling the
    method *next_state*.
    """
    def __init__(self, current_state=None, previous_state=None):
        """
        Creates a new AbstractStateMachine.

        :param current_state: The current state or None. If None is handed over, the
            current state is chosen randomly.
        :param previous_state: The previous state or None.
        """
        self.valid_states = self._get_valid_states()
        self._validate_state(current_state)
        self._validate_state(previous_state)

        if current_state is None:
            self.current_state = self._random_state(self.valid_states)
        else:
            self.current_state = current_state
        self.previous_state = previous_state

    @abstractmethod
    def next_state(self):
        """
        This method moves the machine to the next state based on the current state
        and the previous state.

        :return: The next state and possibly an output.
        """

    @abstractmethod
    def _get_valid_states(self):
        """
        This method returns a set with all valid states.
        :return: The set of valid states.
        """

    def _validate_state(self, state):
        """
        This method validates a certain state. A state is considered valid
        if it is either None or in the set of valid states. If a state is not valid
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
        This function returns a randomly chosen state of a sequence.

        :param states: The sequence of states.
        :return: The randomly chosen state.
        """
        return random.sample(states, k=1)[0]

    def __str__(self):
        return "{previous:" + str(self.previous_state) + ", "\
               "current:" + str(self.current_state) + "}"


# pylint: disable=too-few-public-methods
# Having only one public method is ok
class LeadingBitsMachine(AbstractStateMachine):
    """
    This finite state machine models the transitions between the leading three
    bits of odd Collatz numbers. The machine is a nondeterministic transducer whose states
    represent the bits. As input, the automaton receives the previous state
    or *None* if no previous state exists. As output the machine returns
    the growth of the binary number (lambda) as described in
    (https://doi.org/10.18052/www.scipress.com/IJPMS.21.1)

    The machine only works for the Collatz problem in its original form *3v+1*.
    """

    def _get_valid_states(self):
        return {"100", "101", "110", "111"}

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
