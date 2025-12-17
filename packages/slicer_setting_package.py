import struct
import time

from .package import Package


class SlicerSettingPackage(Package):
    """A package for transferring slicer settings updates and requests."""
    def __init__(
            self,
            timestamp: int = time.time(),
            action: str = "",
            key: str = "",
            value: str = ""
    ):
        """Creates a slicer setting package.

        :param action: The action to perform (e.g., 'get', 'set', 'default').
        :param key: The setting key.
        :param value: The setting value.
        """
        # Using 0x0A (10) as the identifier
        # Format: ! (Network), I (Size), B (ID), L (Timestamp), I (Action Len), I (Key Len), I (Value Len)
        super().__init__(0x0A, "!IBLIII")

        self.timestamp = timestamp
        self.action = action
        self.key = key
        self.value = str(value)  # Ensure value is a string for transport

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        action_bytes = self.action.encode("utf-8")
        key_bytes = self.key.encode("utf-8")
        value_bytes = self.value.encode("utf-8")

        package_format = self.format + f"{len(action_bytes)}s{len(key_bytes)}s{len(value_bytes)}s"

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(action_bytes),
            len(key_bytes),
            len(value_bytes),
            action_bytes,
            key_bytes,
            value_bytes
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a SlicerSettingPackage."""
        identifier = data[4]

        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        # Read the fixed header size
        header_size = struct.calcsize(self.format)
        package = struct.unpack(self.format, data[0:header_size])

        timestamp = package[2]
        action_len = package[3]
        key_len = package[4]
        value_len = package[5]

        # Extract strings
        current_pos = header_size
        action = data[current_pos:current_pos + action_len].decode("utf-8")
        current_pos += action_len

        key = data[current_pos:current_pos + key_len].decode("utf-8")
        current_pos += key_len

        value = data[current_pos:current_pos + value_len].decode("utf-8")

        return SlicerSettingPackage(
            timestamp=timestamp,
            action=action,
            key=key,
            value=value
        )
