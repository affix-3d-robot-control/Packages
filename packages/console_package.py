import struct
import time

from .package import Package


class ConsolePackage(Package):
    """A data package for transferring console_msg information."""

    def __init__(self, timestamp: int = time.time(), console_msg: str = ""):
        """Creates a console_msg package.

        :param console_msg: The binary content of the console_msg file.
        """
        super().__init__(0x09, "!IBLI")

        self.timestamp = timestamp
        self.console_msg = console_msg

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        # Ensure console_msg is bytes
        if isinstance(self.console_msg, str):
            console_msg_bytes = self.console_msg.encode("utf-8")
        else:
            console_msg_bytes = self.console_msg

        package_format = self.format + f"{len(console_msg_bytes)}s"

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(console_msg_bytes),
            console_msg_bytes
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a console_msgPackage.

        :param data: The data package
        :return: The bytes object as a console_msgPackage
        """
        identifier = data[4]

        # Check if identifier matches this package
        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        package = struct.unpack(self.format, data[0:struct.calcsize(self.format)])

        # Convert bytes to correct data
        timestamp = package[2]

        # Extract the remaining data as bytes (do not decode)
        console_msg_data = data[struct.calcsize(self.format):]

        return ConsolePackage(timestamp=timestamp, console_msg=console_msg_data)
