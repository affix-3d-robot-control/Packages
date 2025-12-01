from typing import Tuple


class Robot:
    """Controls the robot."""
    name: str = ""
    code_file: str = ""
    model: str = ""
    brand: str = ""
    axis: int = 0,
    reach: int = 0,
    payload: int = 0,
    weight: int = 0,
    accuracy: float = 0.0,

    def move(
            self,
            location: Tuple[int, int, int],
            rotation: Tuple[float, float, float, float]
    ):
        """Move the robot affector to the given location and rotation.

        :param location: The X, Y, Z location of the robot.
        :param rotation: The W, X, Y, Z rotation of the robot.
        """
        pass
