import struct
import time

from .package import Package


class SelectedRobotPackage(Package):
    """A data package for transferring robot name."""

    def __init__(
            self,
            timestamp: int = time.time(),
            model_brand: str = "",
    ):
        """Creates a selected robot package."""
        super().__init__(0x010, "!IBLI")

        self.timestamp = timestamp
        self.model_brand = model_brand

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = self.format + f"{len(self.model_brand)}s"

        return struct.pack(
            package_format,
            struct.calcsize(package_format),
            self.identifier,
            int(self.timestamp),
            len(self.model_brand),
            self.model_brand.encode("utf-8")
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a SelectedRobotPackage.

        :param data: The data package
        :return: The bytes object as a SelectedRobotPackage
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
        model_brand_size = package[3]

        name = struct.unpack(
            f"{model_brand_size}s",
            data[
                header_size:header_size + model_brand_size
            ])

        return SelectedRobotPackage(
            timestamp=timestamp,
            model_brand=name[0].decode("utf-8")
        )
