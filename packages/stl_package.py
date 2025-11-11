import struct
import time

from .package import Package


class STLPackage(Package):
    """A data package for transferring stl information."""

    def __init__(self, timestamp: int = time.time(), stl: str = ""):
        """Creates a stl package."""
        super().__init__(0x03, "!IBLI")

        self.timestamp = timestamp
        self.stl = stl

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = self.format + f"{len(self.stl)}s"
        stl_bytes = self.stl.encode("utf-8")

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(stl_bytes),
            stl_bytes
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a STLPackage.

        :param data: The data package
        :return: The bytes object as a STLPackage
        """
        identifier = data[4]

        # Check if identifier matches this package
        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        package = struct.unpack(self.format, data[0:struct.calcsize(self.format)])

        # Convert bytes to correct data
        timestamp = package[2]

        stl = data[struct.calcsize(self.format):].decode("utf-8")

        return STLPackage(timestamp=timestamp, stl=stl)
