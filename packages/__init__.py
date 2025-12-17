from .button_package import ButtonPackage
from .config_package import ConfigPackage
from .confirmation_package import ConfirmationPackage
from .console_package import ConsolePackage
from .package import Package
from .progress_package import ProgressPackage
from .request_robot_list_package import RequestRobotListPackage
from .robot_data_package import RobotDataPackage
from .selected_robot_package import SelectedRobotPackage
from .slicer_setting_package import SlicerSettingPackage
from .stl_package import STLPackage
from .temperature_package import TemperaturePackage

PACKAGES = {
    TemperaturePackage().identifier: TemperaturePackage,
    ProgressPackage().identifier: ProgressPackage,
    STLPackage().identifier: STLPackage,
    ConfigPackage().identifier: ConfigPackage,
    RobotDataPackage().identifier: RobotDataPackage,
    SelectedRobotPackage().identifier: SelectedRobotPackage,
    RequestRobotListPackage().identifier: RequestRobotListPackage,
    ConfirmationPackage().identifier: ConfirmationPackage,
    ButtonPackage().identifier: ButtonPackage,
    ConsolePackage().identifier: ConsolePackage,
    SlicerSettingPackage().identifier: SlicerSettingPackage
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
