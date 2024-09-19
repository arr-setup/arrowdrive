# ArrowDrive (adrv)

ArrowDrive is a Python module that allows you to create and manage virtual disks. The module ensures that the virtual disk's size does not exceed a specified maximum limit.

## Version

- Current version: 1.4.2
- Last supported version: 1.4.0

## Installation

ArrowDrive is available on PyPI. You can install it using pip:

```bash
pip install adrv
```

Alternatively, you can clone the repository:

```bash
git clone https://github.com/arr-setup/arrowdrive.git
```

## Usage

### Initialization

Create a new instance of the `Disk` class:

```python
import adrv

disk = adrv.Disk(name='myDisk', path='./disks', max_size=1000 ** 2)
```

### `adrv.Disk(name: str = 'vDisk', path: str = './', max_size: int = 1000 ** 2)`

Initializes a Disk instance.

- **name**: The name of the disk. Defaults to 'vDisk'.
- **path**: The path where the disk will be stored. Defaults to './'.
- **max_size**: The maximum size of the disk in bytes. Defaults to 1,000,000 bytes.
  
### Methods

### `read(vPath: str) -> FileResponse`

Reads a file from the disk.

- **vPath**: The path of the file to be read.

### `write(vPath: str, content: str | bytes = b'', mode: str = 'a') -> int`

Writes content to a file in the disk.

- **vPath**: The path where the content will be written.
- **content**: The content to be written. Defaults to an empty byte string.
- **mode**: The writing mode ('a' for append, 'w' for write). Defaults to 'a'.

### `delete(vPath: str) -> int`

Deletes a file from the disk.

- **vPath**: The path of the file to be deleted.

### `format_disk(modelPath: str | None = None)`

Formats the disk. Optionally, a model path can be provided to initialize the disk with predefined files.

- **modelPath**: The path to a model zip file. None (default) means the Disk will be completely reset.

### `extract_all(target: str)`

Extracts all files from the disk to a target directory.

- **target**: The target directory.

### `f_list(include_ts: bool = False, sys: bool = False) -> list[str | dict]`

Lists files in the disk.

- **include_ts**: Whether to include timestamps (and additional info in future versions). Defaults to False.
- **sys** (deprecated): Whether to include system files. Defaults to False.

### `diagnosis(snooze: bool = False) -> DiagnoseResponse`

Evaluates the health of the disk.

- **snooze**: Whether to suppress output. Defaults to False.

## Example

```python
import adrv

# Create a new disk
disk = adrv.Disk(name='myDisk', path='./storage', max_size=1000**2)

# Write a file
disk.write('hello.txt', 'Hello, world!', mode='w')

# Read a file
file = disk.read('hello.txt')
print(file.content.decode())

# List files
files = disk.f_list()
print(files)

# Delete a file
disk.delete('hello.txt')
```

## Error Handling

The module raises specific exceptions for different error conditions:

- `FileIsDirectoryError`: Raised when attempting to read a directory as a file.
- `FileNotFoundError`: Raised when a file is not found.
- `FullDiskError`: Raised when attempting to write content that exceeds the disk's maximum size.
- `BrokenDiskError`: Raised when the disk is detected to be in a corrupted state.

## Utils

### `utils.parser`

#### `parse(data: str, keys: list, mode: int = 1) -> list | dict | list[dict]`

Parses the provided data string into different formats based on the mode.

- **data**: The data string to parse.
- **keys**: A list of keys to use in the parsing.
- **mode**: Determines the parsing strategy.
  - `1`: Splits data by new lines and zips with keys.
  - `2`: Splits data by new lines and then by '=' for key-value pairs.
  - `3`: Splits data by '::' and optionally zips with keys.
  - `4`: Splits data by new lines.

Returns a list, dictionary, or list of dictionaries based on the mode.

#### `unparse(data, mode: int = 1) -> str`

Unparses data into a string based on the mode.

- **data**: The data to unparse.
- **mode**: Determines the unparse strategy.
  - `1`: Joins values with new lines.
  - `2`: Joins key-value pairs with '=' and new lines.
  - `3`: Joins dictionary values with '::'.
  - `4`: Joins list items with new lines.

Returns the unparsed string.

### `utils.units`

#### `Size`

A class to handle size representation and conversion.

- **__init__(value: int | float)**
  - **value**: The size value in bytes.

- **literal() -> str**
  - Converts the raw size value to a human-readable format (e.g., 1kB, 1MB).

#### Units

- `units`: 1 byte.
- `kilo`: 1 kilobyte (1,000 bytes).
- `mega`: 1 megabyte (1,000,000 bytes).
- `giga`: 1 gigabyte (1,000,000,000 bytes).
- `tera`: 1 terabyte (1,000,000,000,000 bytes).

#### `convert(val: float, _from: str, _to: str) -> float`

Converts a value from one unit to another.

- **val**: The value to convert.
- **_from**: The original unit (B, kB, MB, GB, TB).
- **_to**: The target unit (B, kB, MB, GB, TB).

Returns the converted value.

### `bridge`

#### `PhysicalBridge`

A class to handle physical file transfer to and from the virtual disk.

- **__init__(disk: Disk)**
  - **disk**: The Disk instance to interact with.

- **bring(vPath: str, newPath: str)**
  - Transfers a file from the virtual disk to a physical location.
  - **vPath**: The virtual path of the file.
  - **newPath**: The physical path where the file will be saved.

- **send(filePath: str, vPath: str)**
  - Transfers a file from a physical location to the virtual disk.
  - **filePath**: The physical path of the file.
  - **vPath**: The virtual path where the file will be saved.

#### `VirtualBridge`

A class to handle file transfer between two virtual disks.

- **__init__(firstDisk: Disk, secondDisk: Disk)**
  - **firstDisk**: The source Disk instance.
  - **secondDisk**: The destination Disk instance.

- **cross(targetPath: str, finalPath: str = '/shore', rtl: bool = False)**
  - Transfers a file from one virtual disk to another.
  - **targetPath**: The path of the file on the source disk.
  - **finalPath**: The path where the file will be saved on the destination disk.
  - **rtl**: If `True`, transfers from the second disk to the first; otherwise, transfers from the first to the second.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the GPLv3 License.