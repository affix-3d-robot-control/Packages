from packages import Package


def test_package_initializes():
    """Tests if the base package class initializes."""
    assert Package() is not None
    assert Package(0x01) is not None
    assert Package(struct_format="!IBI") is not None
