from packages.packages import TemperaturePackage


def test_temperature_package_initializes():
    """Tests if the temperature package initializes."""
    assert TemperaturePackage() is not None
    assert TemperaturePackage(1762330645) is not None
    assert TemperaturePackage(temperature=43.8) is not None


def test_temperature_package_converts_to_bytes():
    """Tests if the progress package converts to bytes."""
    package = TemperaturePackage(1762330645, 43.8)
    print(package.to_bytes())
    assert package.to_bytes() == bytes([
        0x00, 0x00, 0x00, 0x11,  # Package Size
        0x01,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x40, 0x45, 0xE6, 0x66, 0x66, 0x66, 0x66, 0x66  # Temperature (43.8)
    ])


def test_bytes_converts_to_temperature_package():
    """Tests if the bytes temperature package converts \
    to the object temperature package."""
    data = bytes([
        0x00, 0x00, 0x00, 0x11,  # Package Size
        0x01,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x40, 0x45, 0xE6, 0x66, 0x66, 0x66, 0x66, 0x66  # Temperature (43.8)
    ])
    package = TemperaturePackage().to_package(data)

    assert package.timestamp == 1762330645
    assert package.temperature == 43.8
