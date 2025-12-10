import struct
import time

from .package import Package
from .robot import Robot


class RobotDataPackage(Package):
    """A data package for transferring robot information."""

    def __init__(
            self,
            timestamp: int = time.time(),
            model: str = "",
            brand: str = "",
            axis: int = 0,
            reach: int = 0,
            payload: int = 0,
            weight: int = 0,
            accuracy: float = 0.0

    ):
        """Creates a robot package."""
        super().__init__(0x05, "!IBLLLLLLLf")

        self.timestamp = timestamp
        self.model = model
        self.brand = brand
        self.axis = axis
        self.reach = reach
        self.payload = payload
        self.weight = weight
        self.accuracy = accuracy

    def from_robot(self, robot: Robot):
        """Converts a robot to RobotDataPackage."""
        return RobotDataPackage(
            timestamp=self.timestamp,
            model=robot.model,
            brand=robot.brand,
            axis=robot.axis,
            reach=robot.reach,
            payload=robot.payload,
            weight=robot.weight,
            accuracy=robot.accuracy
        )

    def to_robot(self):
        """Converts a robot to RobotDataPackage."""
        robot = Robot()
        robot.model = self.model
        robot.brand = self.brand
        robot.axis = self.axis
        robot.reach = self.reach
        robot.payload = self.payload
        robot.weight = self.weight
        robot.accuracy = self.accuracy

        return robot

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = self.format + f"{len(self.model)}s" + f"{len(self.brand)}s"

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(self.model),
            len(self.brand),
            self.axis,
            self.reach,
            self.payload,
            self.weight,
            self.accuracy,
            self.model.encode("utf-8"),
            self.brand.encode("utf-8")
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a RobotDataPackage.

        :param data: The data package
        :return: The bytes object as a RobotDataPackage
        """
        identifier = data[4]

        # Check if identifier matches this package
        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        header_size = struct.calcsize(self.format)

        package = struct.unpack(self.format, data[0:header_size])

        # Convert bytes to correct data
        timestamp = package[2]
        model_size = package[3]
        brand_size = package[4]

        name = struct.unpack(
            f"{model_size}s",
            data[
                header_size:header_size + model_size
            ])

        manufacturer = struct.unpack(
            f"{brand_size}s",
            data[
                header_size + model_size:
                header_size + model_size + brand_size
            ])

        return RobotDataPackage(
            timestamp=timestamp,
            model=name[0].decode("utf-8"),
            brand=manufacturer[0].decode("utf-8"),
            axis=package[5],
            reach=package[6],
            payload=package[7],
            weight=package[8],
            accuracy=round(package[9], 2)
        )
