class Package:
    """The base class for all other packages."""
    def __init__(self, identifier: int = 0, struct_format: str = ""):
        """Initializes all generic attributes of a package."""
        self.identifier = identifier
        self.format = struct_format
