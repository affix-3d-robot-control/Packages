import struct
import time

from backend.robot import Robot
from .package import Package


class RobotDataPackage(Package):
    """A data package for transferring robot information."""

    def __init__(
            self,
            timestamp: int = time.time(),
            name: str = "",
            manufacturer: str = "",
            min_acceleration: float = 0.0,
            max_acceleration: float = 0.0,
            min_speed: float = 0.0,
            max_speed: float = 0.0
    ):
        """Creates a robot package."""
        super().__init__(0x05, "!IBLIIffff")

        self.timestamp = timestamp
        self.name = name
        self.manufacturer = manufacturer
        self.min_acceleration = min_acceleration
        self.max_acceleration = max_acceleration
        self.min_speed = min_speed
        self.max_speed = max_speed

    def from_robot(self, robot: Robot):
        """Converts a robot to RobotDataPackage."""
        return RobotDataPackage(
            timestamp=self.timestamp,
            name=robot.name,
            manufacturer=robot.manufacturer,
            min_acceleration=self.min_acceleration,
            max_acceleration=self.max_acceleration,
            min_speed=self.min_speed,
            max_speed=self.max_speed,
        )

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = self.format + f"{len(self.name)}s" + f"{len(self.manufacturer)}s"

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(self.name),
            len(self.manufacturer),
            self.min_acceleration,
            self.max_acceleration,
            self.min_speed,
            self.max_speed,
            self.name.encode("utf-8"),
            self.manufacturer.encode("utf-8")
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
        name_size = package[3]
        manufacturer_size = package[4]

        name = struct.unpack(
            f"{name_size}s",
            data[
                header_size:header_size + name_size
            ])

        manufacturer = struct.unpack(
            f"{manufacturer_size}s",
            data[
                header_size + name_size:
                header_size + name_size + manufacturer_size
            ])

        return RobotDataPackage(
            timestamp=timestamp,
            name=name[0].decode("utf-8"),
            manufacturer=manufacturer[0].decode("utf-8"),
            min_acceleration=package[5],
            max_acceleration=package[6],
            min_speed=package[7],
            max_speed=package[8],
        )
