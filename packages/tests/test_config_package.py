from packages import ConfigPackage


def test_config_package_initializes():
    """Tests if the config package initializes."""
    assert ConfigPackage() is not None
    assert ConfigPackage(1762330645) is not None
    assert ConfigPackage(key="server.host", value="127.0.0.1") is not None
    assert ConfigPackage(key="server.port", value=8000) is not None
    assert ConfigPackage(key="server.enabled", value=True) is not None
    assert ConfigPackage(key="server.interval", value=25.8) is not None


def test_config_package_converts_to_bytes_str():
    """Tests if the progress package converts to bytes with a string value."""
    package = ConfigPackage(1762330645, "server.host", "127.0.0.1")
    assert package.to_bytes() == bytes([
        0x00, 0x00, 0x00, 0x25,  # Package Size
        0x04,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x00, 0x00, 0x00, 0x0B,  # Key length
        0x00, 0x00, 0x00, 0x09,  # Value length
        0x73, 0x65, 0x72, 0x76, 0x65, 0x72, 0x2e, 0x68, 0x6f, 0x73, 0x74,  # Key (server.host)
        0x31, 0x32, 0x37, 0x2e, 0x30, 0x2e, 0x30, 0x2e, 0x31  # Value (127.0.0.1)
    ])


def test_config_package_converts_to_bytes_int():
    """Tests if the progress package converts to bytes with a int value."""
    package = ConfigPackage(1762330645, "server.port", 8000)
    print(package.to_bytes().hex())
    assert package.to_bytes() == bytes([
        0x00, 0x00, 0x00, 0x20,  # Package Size
        0x04,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x00, 0x00, 0x00, 0x0B,  # Key length
        0x00, 0x00, 0x00, 0x04,  # Value length
        0x73, 0x65, 0x72, 0x76, 0x65, 0x72, 0x2e, 0x70, 0x6F, 0x72, 0x74,  # Key (server.port)
        0x00, 0x00, 0x1F, 0x40  # Value (8000)
    ])


def test_config_package_converts_to_bytes_bool():
    """Tests if the progress package converts to bytes with a bool value."""
    package = ConfigPackage(1762330645, "server.enabled", True)
    print(package.to_bytes().hex())
    assert package.to_bytes() == bytes([
        0x00, 0x00, 0x00, 0x20,  # Package Size
        0x04,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x00, 0x00, 0x00, 0x0E,  # Key length
        0x00, 0x00, 0x00, 0x01,  # Value length
        0x73, 0x65, 0x72, 0x76, 0x65, 0x72, 0x2e, 0x65, 0x6E, 0x61, 0x62, 0x6C, 0x65, 0x64,  # Key (server.enabled)
        0x01  # Value (True)
    ])


def test_config_package_converts_to_bytes_float():
    """Tests if the progress package converts to bytes with a float value."""
    package = ConfigPackage(1762330645, "server.interval", 25.8)
    assert package.to_bytes() == bytes([
        0x00, 0x00, 0x00, 0x24,  # Package Size
        0x04,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x00, 0x00, 0x00, 0x0F,  # Key length
        0x00, 0x00, 0x00, 0x04,  # Value length
        0x73, 0x65, 0x72, 0x76, 0x65, 0x72, 0x2e,  # Key (server.interval)
        0x69, 0x6e, 0x74, 0x65, 0x72, 0x76, 0x61, 0x6c,
        0x41, 0xce, 0x66, 0x66  # Value (25.8)
    ])


def test_bytes_converts_to_config_package_str():
    """Tests if the bytes config package converts \
    to the object config package."""
    data = bytes([
        0x00, 0x00, 0x00, 0x25,  # Package Size
        0x04,  # Identifier
        0x69, 0x0B, 0x08, 0x15,  # Timestamp (1762330645)
        0x00, 0x00, 0x00, 0x0B,  # Key length
        0x00, 0x00, 0x00, 0x09,  # Value length
        0x73, 0x65, 0x72, 0x76, 0x65, 0x72, 0x2e, 0x68, 0x6f, 0x73, 0x74,  # Key (server.host)
        0x31, 0x32, 0x37, 0x2e, 0x30, 0x2e, 0x30, 0x2e, 0x31  # Value (127.0.0.1)
    ])
    package = ConfigPackage().to_package(data)

    assert package.timestamp == 1762330645
    assert package.key == "server.host"
    assert package.value == "127.0.0.1"
