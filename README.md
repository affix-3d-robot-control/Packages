# Packages - Shared Communication Protocol for Affix 3D Robot Control

![Package System](https://img.shields.io/badge/package-system-blue)
![Protocol Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 📋 Table of Contents
- [Overview](#overview)
- [Package Architecture](#package-architecture)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Creating Custom Packages](#creating-custom-packages)
- [Serialization Protocol](#serialization-protocol)
- [Development Guide](#development-guide)
- [Contributing](#contributing)

## Overview

The Packages repository is the shared communication library for the Affix 3D Robot Control system. It defines the standardized data structures, serialization protocols, and message formats used for communication between all system components (Frontend, Backend, and Translation Layer).

### Key Responsibilities:
- **Data Structure Definition**: Standardized classes for all system messages
- **Serialization Protocol**: Binary serialization/deserialization for network transmission
- **Type Safety**: Enforced data types and validation for all messages
- **Version Compatibility**: Protocol version management and backward compatibility
- **Centralized Definition**: Single source of truth for all communication data structures

## Package Architecture

### Communication Flow
```
┌──────────┐    Packages    ┌──────────┐    Packages    ┌───────────┐
│ Frontend │ ◄────────────► │ Backend  │ ◄────────────► │Translation│
└──────────┘    (TCP)       └──────────┘(Library import)└───────────┘
```

### Package Structure
Each package follows this base structure:
```python
class Package:
    def __init__(self, identifier: int, format_string: str):
        self.identifier = identifier  # Unique package type ID
        self.format = format_string   # Struct format for serialization
        
    def to_bytes(self) -> bytes:
        """Serialize package to binary format"""
        
    def to_package(self, data: bytes):
        """Deserialize binary data to package"""
```

### Key Components
1. **Package Base Class**: Abstract base class for all packages
2. **Identifier System**: Unique hex codes for each package type
3. **Struct Format**: Python struct module format strings for serialization
4. **Validation Logic**: Type checking and data validation

## Installation

### As a Git Submodule (Recommended)
The packages repository is designed to be used as a submodule in other projects:

#### 1. Add to Your Repository
```bash
# Add as a submodule
git submodule add https://github.com/affix-3d-robot-control/packages.git ./packages
```

#### 2. Initialize Existing Submodules
```bash
# If submodule already exists in repository
git submodule update --recursive --init
```

#### 3. Update to Latest Version
```bash
# Pull latest changes
git submodule update --recursive --remote
```

#### 4. Using Poetry with Submodules
Add to your `pyproject.toml`:
```toml
[virtualenvs]
in-project = true
```

### Direct Installation (Development)
```bash
# Clone the repository
git clone https://github.com/affix-3d-robot-control/packages.git
cd packages

# Install with Poetry
poetry install

# Or install with pip
pip install -e .
```

## Usage Guide

### Basic Usage Pattern

#### 1. Import and Create Package
```python
from packages.src.button_package import ButtonPackage

# Create a button press package
button_package = ButtonPackage(
    timestamp=time.time(),
    button_name="emergency_stop"
)

# Serialize to bytes for transmission
binary_data = button_package.to_bytes()
```

#### 2. Send Over Network
```python
# Example TCP sending
import socket

def send_package(host, port, package):
    data = package.to_bytes()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(data)
```

#### 3. Receive and Deserialize
```python
# Example TCP receiving
def receive_package(socket):
    # First read the size (first 4 bytes)
    size_bytes = socket.recv(4)
    if not size_bytes:
        return None
    
    # Read the rest of the package
    size = struct.unpack("!I", size_bytes)[0]
    data = size_bytes + socket.recv(size - 4)
    
    # Determine package type and deserialize
    identifier = data[4]  # 5th byte is package identifier
    if identifier == 0x08:  # ButtonPackage
        from packages.src.button_package import ButtonPackage
        return ButtonPackage().to_package(data)
    # ... handle other package types
```

### Detailed Package Example

#### ButtonPackage (0x08)
```python
from .package import Package


class ButtonPackage(Package):
    """A package for transferring button press information."""

    def __init__(self, timestamp: int = time.time(), button_name: str = ""):
        """Creates the button package."""
        # Using 0x08 as the identifier
        super().__init__(0x08, "!IBLI")

        self.timestamp = timestamp
        self.button_name = button_name

    def to_bytes(self) -> bytes:
        """Converts the current package to a bytes object."""
        package_format = self.format + f"{len(self.button_name)}s"
        name_bytes = self.button_name.encode("utf-8")

        return struct.pack(
            package_format,
            struct.calcsize(package_format),  # Item 1: Size (I)
            self.identifier,                  # Item 2: ID (B)
            int(self.timestamp),              # Item 3: Timestamp (L)
            len(name_bytes),                  # Item 4: Length (I) - This was missing in the format!
            name_bytes                        # Item 5: String (s)
        )

    def to_package(self, data: bytes):
        """Convert a bytes object into a ButtonPackage."""
        identifier = data[4]

        if identifier != self.identifier:
            raise ValueError(f"Package identifier for {__name__} "
                             f"must be {self.identifier}. Found {identifier}")

        # Read the fixed header size
        header_size = struct.calcsize(self.format)
        package = struct.unpack(self.format, data[0:header_size])

        timestamp = package[2]

        # Read the rest of the data as the string
        button_name = data[header_size:].decode("utf-8")

        return ButtonPackage(timestamp=timestamp, button_name=button_name)
```

## Creating Custom Packages

### Step-by-Step Guide

#### 1. Define Package Class
```python
import struct
import time
from .package import Package

class CustomPackage(Package):
    """Example custom package."""
    
    def __init__(self, custom_data: str = "", number: int = 0):
        # Choose unique identifier (0x80-0xFF for custom packages)
        super().__init__(0x80, "!IBI")
        self.custom_data = custom_data
        self.number = number
    
    def to_bytes(self) -> bytes:
        """Serialize package to bytes."""
        package_format = self.format + f"{len(self.custom_data)}s"
        data_bytes = self.custom_data.encode("utf-8")
        
        return struct.pack(
            package_format,
            struct.calcsize(package_format),  # Size (I)
            self.identifier,                  # ID (B)
            self.number,                      # Number (I)
            data_bytes                        # String (s)
        )
    
    def to_package(self, data: bytes):
        """Deserialize bytes to package."""
        identifier = data[4]
        if identifier != self.identifier:
            raise ValueError(f"Wrong package identifier: {identifier}")
        
        # Unpack fixed header
        header_size = struct.calcsize(self.format)
        package = struct.unpack(self.format, data[0:header_size])
        
        # Get variable string
        str_length = package[2]  # Third element in format
        custom_data = data[header_size:header_size + str_length].decode("utf-8")
        
        return CustomPackage(
            custom_data=custom_data,
            number=package[2]
        )
```

#### 2. Add to Package Registry
```python
# In packages/src/__init__.py
from .custom_package import CustomPackage

PACKAGES = [
    'ButtonPackage',
    'SlicerSettingPackage',
    ...
    'CustomPackage',  # Add your custom package
]
```

## Serialization Protocol

### Binary Format Specification

#### Header Structure
```
Byte Offset | Size | Type   | Description
------------|------|--------|-------------
0-3         | 4    | uint32 | Total package size (including header)
4           | 1    | uint8  | Package identifier (0x00-0xFF)
5+          | var  | -      | Package-specific data
```

#### Struct Format Characters
| Character | C Type | Python Type | Size |
|-----------|--------|-------------|------|
| `x` | pad byte | no value | 1 |
| `c` | char | bytes of length 1 | 1 |
| `b` | signed char | integer | 1 |
| `B` | unsigned char | integer | 1 |
| `?` | _Bool | bool | 1 |
| `h` | short | integer | 2 |
| `H` | unsigned short | integer | 2 |
| `i` | int | integer | 4 |
| `I` | unsigned int | integer | 4 |
| `l` | long | integer | 4 |
| `L` | unsigned long | integer | 4 |
| `q` | long long | integer | 8 |
| `Q` | unsigned long long | integer | 8 |
| `f` | float | float | 4 |
| `d` | double | float | 8 |
| `s` | char[] | bytes | 1 per char |
| `p` | char[] | bytes | 1 per char + 1 |
| `P` | void * | integer | platform |

### Endianness
All packages use **network byte order** (big-endian) indicated by the `!` prefix in format strings:
- `!`: Network byte order (big-endian)
- Ensures compatibility across different architectures

## Development Guide

### Setting Up Development Environment

#### 1. Clone Repository
```bash
git clone https://github.com/affix-3d-robot-control/packages.git
cd packages
```

#### 2. Install Development Dependencies
```bash
poetry install

# Install pre-commit hooks
poetry run pre-commit install
```

#### 3. Run Tests
```bash
# Package tests
poetry run pytest tests/your-test
```

### Adding New Packages

#### 1. Create New Package File
```python
# In src/packages/custom_category/new_package.py
import struct
import time
from ..package import Package

class NewPackage(Package):
    """Description of new package."""
    
    def __init__(self, param1: str = "", param2: int = 0):
        # Choose unused identifier (check existing packages)
        super().__init__(0x90, "!IB20sI")
        self.param1 = param1
        self.param2 = param2
    
    def to_bytes(self) -> bytes:
        return struct.pack(
            self.format,
            struct.calcsize(self.format),
            self.identifier,
            self.param1.encode("utf-8"),
            self.param2
        )
    
    def to_package(self, data: bytes):
        identifier = data[4]
        if identifier != self.identifier:
            raise ValueError(f"Wrong identifier: {identifier}")
        
        package = struct.unpack(self.format, data)
        return NewPackage(
            param1=package[2].decode("utf-8").strip('\x00'),
            param2=package[3]
        )
```

## Contributing

### Development Workflow

#### 1. Fork Repository
```bash
git fork https://github.com/affix-3d-robot-control/packages.git
cd packages
```

#### 2. Create Feature Branch
```bash
git checkout -b feature/new-package-type
```

#### 3. Make Changes
- Add new packages or modify existing ones
- Update tests
- Update documentation

#### 4. Run Quality Checks
```bash
# Code formatting
poetry run black src/ tests/

# Linting
poetry run flake8 src/ tests/

# Type checking
poetry run mypy src/

# Run tests
poetry run pytest tests/ -v
```

#### 5. Submit Pull Request
- Include clear description of changes
- Reference related issues
- Ensure all tests pass
- Update README if necessary

### Code Standards

#### Package Design Guidelines
1. **Single Responsibility**: Each package should handle one specific type of data
2. **Immutability**: Packages should be immutable after creation
3. **Validation**: Validate data in constructor and serialization methods
4. **Documentation**: Include docstrings for all public methods
5. **Testing**: Write unit tests for serialization/deserialization

#### Identifier Allocation
- **0x00-0x07**: Reserved for system use
- **0x08-0x7F**: Core system packages
- **0x80-0xBF**: Extended system packages
- **0xC0-0xFF**: Custom/experimental packages

### Release Process

#### 1. Update Version
```bash
# Update pyproject.toml version
# Update __version__ in src/packages/__init__.py
```

#### 2. Update Changelog
```markdown
## [1.1.0] - 2026-01-20
### Added
- New CustomPackage for extended functionality
### Changed
- Improved serialization performance
### Fixed
- Bug in ButtonPackage string encoding
```

#### 3. Create Release Tag
```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

#### 4. Update Submodules
```bash
# In dependent repositories
git submodule update --recursive --remote
```

## Support

### Getting Help
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Package development guide
- **Email**: i.oz@affixengineering.nl

### When Reporting Issues
Please include:
1. Package version
2. Python version
3. Error message and stack trace
4. Steps to reproduce
5. Sample code if possible

---

**Version**: 1.0.0  
**Last Updated**: January 20, 2026  
**License**: MIT License  
**Repository**: https://github.com/affix-3d-robot-control/packages

*For more information, visit the [main project repository](https://github.com/affix-3d-robot-control).*
</pre>
