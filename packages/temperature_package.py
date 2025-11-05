import struct
import time

from packages.package import Package


class TemperaturePackage(Package):
    """A data package for transferring temperature information."""

    def __init__(self, timestamp: int = time.time(), temperature: float = 0.0):
        """Creates a temperature package."""
        super().__init__(0x01, "!IBLd")

        self.timestamp = timestamp
        self.temperature = temperature

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        return struct.pack(
            self.format,
            struct.calcsize(self.format),
            self.identifier,
            int(self.timestamp),
            self.temperature
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a TemperaturePackage.

        :param data: The data package
        :return: The bytes object as a TemperaturePackage
        """
        identifier = data[4]

        # Check if identifier matches this package
        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        package = struct.unpack(self.format, data)

        # Convert bytes to correct data
        timestamp = package[2]
        temperature = package[3]

        return TemperaturePackage(timestamp=timestamp, temperature=temperature)
