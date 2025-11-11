import struct
import time

from .package import Package


class ConfigPackage(Package):
    """A data package for transferring config information."""

    def __init__(
            self,
            timestamp: int = time.time(),
            key: str = "",
            value: int | str | bool | float = ""
    ):
        """Creates a config package."""
        super().__init__(0x04, "!IBLII")

        self.timestamp = timestamp
        self.key = key
        self.value = value

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = (
            self.format + f"{len(self.key)}s{len(self.value)}s" if type(self.value) is str else
            self.format + f"{len(self.key)}sl" if type(self.value) is int else
            self.format + f"{len(self.key)}sf" if type(self.value) is float else
            self.format + f"{len(self.key)}s?"
        )

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(self.key),
            len(self.value) if type(self.value) is str else 1 if type(self.value) is bool else 4,
            self.key.encode("utf-8"),
            self.value.encode("utf-8") if type(self.value) is str else self.value
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a ConfigPackage.

        :param data: The data package
        :return: The bytes object as a ConfigPackage
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
        key_size = package[3]
        value_size = package[4]

        print(data[header_size:header_size + key_size])

        key = struct.unpack(f"{key_size}s", data[header_size:header_size + key_size])
        value = struct.unpack(f"{value_size}s", data[header_size + key_size:])

        return ConfigPackage(timestamp=timestamp, key=key[0].decode("utf-8"), value=value[0].decode("utf-8"))
