import struct
import time

from .package import Package


class SlicerConfigFilePackage(Package):
    """A package for transferring the full slicer_config.ini content."""

    def __init__(self, timestamp: int = time.time(), config_content: str = ""):
        """Creates the slicer config file package."""
        # Using 0x09 as the identifier
        super().__init__(0x09, "!IBLI")

        self.timestamp = timestamp
        self.config_content = config_content

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        content_bytes = self.config_content.encode("utf-8")
        package_format = self.format + f"{len(content_bytes)}s"

        return struct.pack(
            package_format,
            struct.calcsize(package_format),  # Item 1: Size (I)
            self.identifier,                  # Item 2: ID (B)
            int(self.timestamp),              # Item 3: Timestamp (L)
            len(content_bytes),               # Item 4: Length (I)
            content_bytes                     # Item 5: String (s)
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a SlicerConfigFilePackage."""
        identifier = data[4]

        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        # Read the fixed header size
        header_size = struct.calcsize(self.format)
        package = struct.unpack(self.format, data[0:header_size])

        timestamp = package[2]

        # Read the rest of the data as the string
        config_content = data[header_size:].decode("utf-8")

        return SlicerConfigFilePackage(timestamp=timestamp, config_content=config_content)