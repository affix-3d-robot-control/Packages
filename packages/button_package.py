import struct
import time
from .package import Package

class ButtonPackage(Package):
    """A package for transferring button press information."""

    def __init__(self, timestamp: int = time.time(), button_name: str = ""):
        """Creates the button package."""
        # Using 0x08 as the identifier
        super().__init__(0x08, "!IBL") 
        
        self.timestamp = timestamp
        self.button_name = button_name

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = self.format + f"{len(self.button_name)}s"
        name_bytes = self.button_name.encode("utf-8")

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(name_bytes),
            name_bytes
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
        
        # Read the rest of the data as the string
        button_name = data[header_size:].decode("utf-8")

        return ButtonPackage(timestamp=timestamp, button_name=button_name)