from typing import NamedTuple, Tuple


class _RobotAcceleration(NamedTuple):
    min_acceleration: float
    max_acceleration: float


class _RobotSpeed(NamedTuple):
    min_speed: float
    max_speed: float


class Robot:
    """Controls the robot."""
    name: str = ""
    code_file: str = ""
    manufacturer: str = ""
    acceleration: _RobotAcceleration
    speed: _RobotSpeed

    def move(self, location: Tuple[int, int, int], rotation: Tuple[float, float, float, float]):
        """Move the robot affector to the given location and rotation.

        :param location: The X, Y, Z location of the robot.
        :param rotation: The W, X, Y, Z rotation of the robot.
        """
        pass