from typing import Tuple


class Robot:
    """Controls the robot."""
    name: str = ""
    code_file: str = ""
    model: str = ""
    brand: str = ""
    material: str = ""
    axis: int = 0,
    reach: int = 0,
    payload: int = 0,
    weight: int = 0,
    accuracy: float = 0.0,

    def connect(self):
        """Connects to the robot."""
        pass

    def disconnect(self):
        """Disconnects from the robot."""
        pass

    def abort_all(self):
        """Aborts all programs running on a physical robot."""
        pass

    def curpos(self):
        """Gets current position in pose of robot."""
        pass

    def curjpos(self):
        """Gets current position in joints of robot."""
        pass

    def movePose(
            self,
            location: Tuple[int, int, int],
            rotation: Tuple[float, float, float, float]
    ):
        """Move the robot affector to the given location and rotation via pose.

        :param location: The X, Y, Z location of the robot.
        :param rotation: The W, X, Y, Z rotation of the robot.
        """
        pass

    def moveJoint(
            self,
            joints: Tuple[float, float, float, float, float]
    ):
        """Move the robot affector to the given location and rotation via joint.

        :param joints: The values for each joint.
        """
        pass
