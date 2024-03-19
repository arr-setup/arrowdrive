# ArrowDrive
Special reader for ArrowBit virtual disks.
vDisk extension: `.adrv`

# How to use it

## 1- Create a Disk object
```py
from adrv import Disk

myDisk = Disk('myDisk', './vDisks', 4 * 1000 ** 3) # Create a 4GB disk.
```

**Parameters:**
> `name: str` - The name of the vDisk<br>
> `path: str` - The directory where the vDisk will be created<br>
> `size: int` - the size of the vDisk, in bytes<br>

You just created a new Disk object that points to the given path. If the disk doesn't exist, it will be created with the necessary directories.<br>
**Important:** The 4GB limit set up isn't pre-allocated and it's only a virtual limit. It can easily be edited with the class attributes (it should be fixed soon)

## 2- Create a file...

### With the PhysicalBridge

The PhysicalBridge is a bridge between your computer's file system and the virtual disk. With it, you can copy a file from your working directory or another on your computer and your removable storage and vice-versa.

```py
from adrv import Disk
from adrv.bridge import PhysicalBridge

myDisk = Disk('myDisk', './vDisks', 4 * 1000 ** 3) # Create a 4GB disk.
bridge = PhysicalBridge(myDisk)

bridge.send('./images/drawing.png', '/drawings')
```

**PhysicalBridge.send() - Parameters:**
> `filePath: str` - The file absolute or relative path on your computer<br>
> `virtualPath: str` - The destination of your file in the virtual disk<br>
> `newName: str` *(optional)* - The new name of the file, default is the last element of the `filePath` value.<br>

### With the VirtualBridge
You can use the VirtualBridge to transfer a file between two disks with only one method.

```py
from adrv import Disk
from adrv.bridge import VirtualBridge

myDisk = Disk('myDisk', './vDisks', 4 * 1000 ** 3) # Create a 4GB disk.
yourDisk = Disk('yourDisk', './vDisks', 4 * 1000 ** 3) # Create another 4GB disk.
vBridge = VirtualBridge(myDisk, yourDisk)

vBridge.cross('/images/drawing.png', '/drawings', rtl = False) # Copy drawing.png on the first disk to the /drawings directory of the second disk
```

**VirtualBridge() - Parameters:**
> `left: Disk` - The default sender Disk<br>
> `right: Disk` - The default receiver Disk<br>

**VirtualBridge.cross() - Parameters:**
> `targetPath: str` - The targeted file path on the **sender**<br>
> `finalPath: str` - The destination path of the file in the **receiver**<br>
> `rtl: bool` _(optional)_ - Choose whether the sender/receiver roles are reversed or not. Default option is False<br>

### Manually
```py
from adrv import Disk

myDisk = Disk('myDisk', './vDisks', 4 * 1000 ** 3) # Create a 4GB disk.
myDisk.write('/hello/world.txt', 'Hello World', 'w') # You can use it in a variable to see how many bytes have been written
```

**Disk.write() - Parameters:**
> `vPath: str` - The file destination on your virtual disk<br>
> `content: str | bytes` - The file content<br>
> `mode: str` _'a' or 'w'_ - Defines whether the file should be overwritten or not<br>

## 3- Read a file

The only way to read a file is the Disk.read() method:
```py
from adrv import Disk

myDisk = Disk('myDisk', './vDisks', 4 * 1000 ** 3) # Create a 4GB disk.
content = myDisk.read('/hello/world.txt')
```

The `file` variable contains a `FileResponse` with 4 attributes:
> `content: str | bytes` - The file content as you wrote it
> `name: str` - The name of the file
> `timestamp: int` - The **virtual file** creation time
> `size: int` - The size of the file

**Disk.read() - Parameters:**
> `vpath: str` - Path of the file to read

## 4- Delete a file

```py
from adrv import Disk

myDisk = Disk('myDisk', './vDisks', 4 * 1000 ** 3) # Create a 4GB disk.
myDisk.delete('/hello/world.txt') # Similary to write(), you can get the amount of bytes removed from the disk
```

**Disk.delete() - Parameters:**
> `vpath: str` - Path of the file to deleted

## 5- Formatting and file system informations
Formatting a Disk is sometimes useful when you have a totally useless file that you want to recycle, or if your disk is broken.

### Basic formatting
The basic formatting overwrites a new, completely blank disk on the old one.<br>
**Be careful before using it: The whole content of your virtual disk will be wipped out, the system files as well (will be rewritten)**

```py
myDisk = Disk('myDisk', './vDisks', 4 * 1000 ** 3) # Create a 4GB disk.
myDisk.format_disc()
```

### Soft formatting
_Available in 1.1_

### What type of formatting to use

|                       	        | Basic formatting   	| Soft formatting    	|
|----------------------------------	|----------------------	|---------------------- |
| Data preservation     	        | ❌ | ✅ |
| Guarenteed efficiency*           	| ✅ | ❌ |
| Generates a new disk if missing   | ❌ | ✅ |
| Convert to another fs (i.g. NTFS) | ❌ | ❌ |
| Copy sys files from another vDisk | ❌ | 🕗 _1.1_ |

_* A guaranteed efficiency means the disk doesn't have any chance to be broken after being formatted._ <br>

According to the table above, the two types of formatting have their own advantages. The basic formatting is recommended in the case you would like to wipe all the content of your disk to make a better one. The soft formatting can be used to create a new disk from a simple ZIP archive.

### Disk status

You can check the status of the disk with a built-in method, and choose whether you want to use it in your code or visually (i.g. for testing)

```py
from adrv import Disk, convert

disk = Disk('myDisk', './disks', convert(4, 'GB'))
disk.format_disk()
disk.diagnosis() # Prints the result (it should be good)

if not disk.diagnosis(snooze = True).result(): # Snooze prevents the method from printing
    print("Your disk is broken")

with open(disk.path, 'w') as file:
    file.write('abc')

disk.diagnosis() # Prints the result again (it should be bad)
```

**Response:**
This method returns a `DiagnoseResponse` with the three following items:<br>
- `disk_format` - Returns whether the file targeted by the Disk is correct or not (it should always be True except if the first formatting failed)
- `is_supported` - Returns whether the disk is supported by your version of ADRV
- `primary_files` - Returns if the necessary system files are in your disk or not (often related with `is_supported`)
- `result()` - Returns True if all of the above items are True

**Note: After a formatting, you have no need to diagnose the disk (it is done automatically)**

### Other methods

**extract_all(target: str):**<br>
Extracts the archive in the given directory (`target`)<br><br>
**f_list(include_ts: bool = False):**<br>
List all the files (`list[str]`) and include their timestamp (`list[dict]`) if `include_ts` is `True`.