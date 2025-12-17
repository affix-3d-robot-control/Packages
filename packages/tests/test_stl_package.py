from packages import STLPackage


def test_stl_package_initializes():
    """Tests if the stl package initializes."""
    assert STLPackage() is not None
    assert STLPackage(1762330645) is not None
    assert STLPackage(stl="/dev/null") is not None


def test_stl_package_converts_to_bytes():
    """Tests if the progress package converts to bytes."""
    package = STLPackage(1762330645, "/dev/null")
    assert package.to_bytes() == bytes([
        0x00, 0x00, 0x00, 0x16,  # Package Size
        0x03,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x00, 0x00, 0x00, 0x09,  # Stl length (9)
        0x2f, 0x64, 0x65, 0x76, 0x2f, 0x6e, 0x75, 0x6c, 0x6c  # Stl (/dev/null)
    ])
