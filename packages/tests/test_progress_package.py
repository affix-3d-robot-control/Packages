from packages import ProgressPackage


def test_progress_package_initializes():
    """Tests if the progress package initializes."""
    assert ProgressPackage() is not None
    assert ProgressPackage(1762330645) is not None
    assert ProgressPackage(progress=43.8) is not None


def test_progress_package_converts_to_bytes():
    """Tests if the progress package converts to bytes."""
    package = ProgressPackage(1762330645, 43.8)
    assert package.to_bytes() == bytes([
        0x00, 0x00, 0x00, 0x11,  # Package Size
        0x01,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x40, 0x45, 0xE6, 0x66, 0x66, 0x66, 0x66, 0x66  # Progress (43.8)
    ])


def test_bytes_converts_to_progress_package():
    """Tests if the bytes package convert to the object package."""
    data = bytes([
        0x00, 0x00, 0x00, 0x11,  # Package Size
        0x01,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x40, 0x45, 0xE6, 0x66, 0x66, 0x66, 0x66, 0x66  # Progress (43.8)
    ])
    package = ProgressPackage().to_package(data)

    assert package.timestamp == 1762330645
    assert package.progress == 43.8
