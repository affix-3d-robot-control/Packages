import struct
import time

from .package import Package


class ConfigPackage(Package):
    """A data package for transferring config information."""

    def __init__(
            self,
            timestamp: int = time.time(),
            section: str = "",
            option: str = "",
            value: int | str | bool | float = ""
    ):
        """Creates a config package."""
        super().__init__(0x04, "!IBLIII")

        self.timestamp = timestamp
        self.section = section
        self.option = option
        self.value = value

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = (
            self.format + f"{len(self.section)}s{len(self.option)}s{len(self.value)}s" if type(self.value) is str else
            self.format + f"{len(self.section)}s{len(self.option)}sl" if type(self.value) is int else
            self.format + f"{len(self.section)}s{len(self.option)}sf" if type(self.value) is float else
            self.format + f"{len(self.section)}s{len(self.option)}s?"
        )

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(self.section),
            len(self.option),
            len(self.value) if type(self.value) is str else 1 if type(self.value) is bool else 4,
            self.section.encode("utf-8"),
            self.option.encode("utf-8"),
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
        section_size = package[3]
        option_size = package[4]
        value_size = package[5]

        print(data[header_size:header_size + section_size])

        section = struct.unpack(
            f"{section_size}s",
            data[
                header_size:header_size + section_size
            ])

        option = struct.unpack(
            f"{option_size}s",
            data[
                header_size + section_size:
                header_size + section_size + option_size
            ])

        value = struct.unpack(
            f"{value_size}s",
            data[
                header_size + section_size + option_size:
            ])

        return ConfigPackage(
            timestamp=timestamp,
            section=section[0].decode("utf-8"),
            option=option[0].decode("utf-8"),
            value=value[0].decode("utf-8")
        )
