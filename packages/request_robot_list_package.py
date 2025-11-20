import struct
import time

from .package import Package


class RequestRobotListPackage(Package):
    """A package to request all loaded robots.."""

    def __init__(self, timestamp: int = time.time(), progress: float = 0.0):
        """Creates a request package."""
        super().__init__(0x06, "!IBL")

        self.timestamp = timestamp

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        return struct.pack(
            self.format,
            struct.calcsize(self.format),
            self.identifier,
            int(self.timestamp)
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a RequestRobotListPackage.

        :param data: The data package
        :return: The bytes object as a RequestRobotListPackage
        """
        identifier = data[4]

        # Check if identifier matches this package
        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        package = struct.unpack(self.format, data)

        # Convert bytes to correct data
        timestamp = package[2]

        return RequestRobotListPackage(timestamp=timestamp)
