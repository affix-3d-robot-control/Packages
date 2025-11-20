import struct
import time

from .package import Package


class ConfirmationPackage(Package):
    """A package to confirm an action was completed successfully."""

    def __init__(self,
                 timestamp: int = time.time(),
                 confirmed_request_id: int = 1,
                 confirmed_request_timestamp: int = 0
                 ):
        """Creates a confirmation package."""
        super().__init__(0x07, "!IBLBL")

        self.timestamp = timestamp
        self.confirmed_request_id = confirmed_request_id
        self.confirmed_request_timestamp = confirmed_request_timestamp

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        return struct.pack(
            self.format,
            struct.calcsize(self.format),
            self.identifier,
            int(self.timestamp),
            self.confirmed_request_id,
            self.confirmed_request_timestamp
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a ConfirmationPackage.

        :param data: The data package
        :return: The bytes object as a ConfirmationPackage
        """
        identifier = data[4]

        # Check if identifier matches this package
        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        package = struct.unpack(self.format, data)

        # Convert bytes to correct data
        timestamp = package[2]
        confirmed_request_id = package[3]
        confirmed_request_timestamp = package[4]

        return ConfirmationPackage(
            timestamp=timestamp,
            confirmed_request_id=confirmed_request_id,
            confirmed_request_timestamp=confirmed_request_timestamp
        )
