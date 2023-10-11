from abc import abstractmethod
from typing import Protocol
import numpy as np


class EnvironemntProtocol(Protocol):
    """The environment protocol"""

    @abstractmethod
    def get_environment_observation(self) -> np.array:
        """Get observation data from the environment"""
        raise NotImplementedError

    @abstractmethod
    def step(self, action: int) -> tuple[int, float, bool, list]:
        """Process the next step/movment in the environment"""
        raise NotImplementedError

    @abstractmethod
    def termination_check(self, new_state_x: int, new_state_y: int) -> bool:
        """Check if the agent action has lead to termination of the agent"""
        raise NotImplementedError

    @abstractmethod
    def process_action(self, action: int) -> tuple[int]:
        """Process the given action"""
        raise NotImplementedError

    @abstractmethod
    def calculate_reward(self, current_state_x: int, current_state_y: int) -> float:
        """Calculate a reward for the given move"""
        raise NotImplementedError

    @abstractmethod
    def remove_goal(self, current_state_x: int, current_state_y: int) -> None:
        """Remove a goal node from the maze once reached"""
        raise NotImplementedError
