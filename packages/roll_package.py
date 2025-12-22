import struct
import time

from .package import Package


class RollPackage(Package):
    """A package for transferring button press information."""

    def __init__(self, timestamp: int = time.time(), degrees: int = 0):
        """Creates the button package."""
        # Using 0x011 as the identifier
        super().__init__(0x011, "!IBLl")

        self.timestamp = timestamp
        self.degrees = degrees

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = self.format
        degree_bytes = self.degrees

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            degree_bytes
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a ButtonPackage."""
        identifier = data[4]

        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        # Read the fixed header size
        header_size = struct.calcsize(self.format)
        package = struct.unpack(self.format, data[0:header_size])

        timestamp = package[2]
        degrees = package[3]

        return RollPackage(timestamp=timestamp, degrees=degrees)
