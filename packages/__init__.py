from .config_package import ConfigPackage
from .package import Package
from .progress_package import ProgressPackage
from .stl_package import STLPackage
from .temperature_package import TemperaturePackage

PACKAGES = {
    TemperaturePackage().identifier: TemperaturePackage,
    ProgressPackage().identifier: ProgressPackage,
    STLPackage().identifier: STLPackage,
    ConfigPackage().identifier: ConfigPackage,
}


def get_package(data: bytes) -> Package:
    """Finds the correct package from the bytes object and returns it."""
    identifier = data[4]

    if identifier not in PACKAGES.keys():
        raise ValueError(f"No package found for data with identifier {identifier}")

    return PACKAGES[identifier]().to_package(data)


def get_identifier(package_type: type[Package]) -> int:
    """Finds the correct package identifier and returns it."""
    return package_type().identifier
