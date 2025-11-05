from .package import Package
from .progress_package import ProgressPackage
from .stl_package import STLPackage
from .temperature_package import TemperaturePackage


def get_package(data: bytes) -> Package:
    """Finds the correct package from the bytes object and returns it."""
    identifier = data[4]

    match identifier:
        case 0x01:
            return TemperaturePackage().to_package(data)
        case 0x02:
            return ProgressPackage().to_package(data)
        case 0x03:
            return STLPackage().to_package(data)

    raise ValueError(f"No package found for data with identifier {identifier}")
