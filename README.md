# ArrowDrive
Special reader for ArrowBit virtual disks.
vDisk extension: `.adrv`

# How to use it

## 1- Create a Disk object
```py
from adrv.disk import Disk

myDisk = Disk('./vDisks/myDisk.adrv', 4 * 1000 ** 3) # Create a 4GB disk.
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
from adrv.disk import Disk
from adrv.bridge import PhysicalBridge

myDisk = Disk('./vDisks/myDisk.adrv', 4 * 1000 ** 3) # Create a 4GB disk.
bridge = PhysicalBridge(myDisk)

bridge.send('./images/drawing.png', '/drawings')
```

**PhysicalBridge.copy() - Parameters:**
> `filePath: str` - The file absolute or relative path on your computer<br>
> `virtualPath: str` - The destination of your file in the virtual disk<br>
> `newName: str` *(optional)* - The new name of the file, default is the last element of the `filePath` value.<br>

### With the VirtualBridge
You can use the VirtualBridge to transfer a file between two disks with only one method.

```py
from adrv.disk import Disk
from adrv.bridge import VirtualBridge

myDisk = Disk('./vDisks/myDisk.adrv', 4 * 1000 ** 3) # Create a 4GB disk.
yourDisk = Disk('./vDisks/yourDisk.adrv', 4 * 1000 ** 3) # Create another 4GB disk.
vBridge = VirtualBridge(myDisk, yourDisk)

vBridge.cross('/images/drawing.png', '/drawings', rtl = False) # Copy drawing.png on the first disk to the /drawings directory of the second disk
```

**VirtualBridge() - Parameters:**
> `left: Disk` - The default sender Disk<br>
> `right: Disk` - The default receiver Disk<br>

**VirtualBridge.copy() - Parameters:**
> `targetPath: str` - The targeted file path on the **sender**<br>
> `finalPath: str` - The destination path of the file in the **receiver**<br>
> `rtl: bool` _(optional)_ - Choose whether the sender/receiver roles are reversed or not. Default option is False<br>

### Manually
```py
from adrv.disk import Disk

myDisk = Disk('./vDisks/myDisk.adrv', 4 * 1000 ** 3) # Create a 4GB disk.
myDisk.write('/hello/world.txt', 'Hello World', 'w') # You can use it in a variable to see how many bytes have been written
```

**Disk.write() - Parameters:**
> `vPath: str` - The file destination on your virtual disk<br>
> `content: str | bytes` - The file content<br>
> `mode: str` _'a' or 'w'_ - Defines whether the file should be overwritten or not<br>

## 3- Read a file

The only way to read a file is the Disk.read() method:
```py
from adrv.disk import Disk

myDisk = Disk('./vDisks/myDisk.adrv', 4 * 1000 ** 3) # Create a 4GB disk.
file = myDisk.read('/hello/world.txt')
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
from adrv.disk import Disk

myDisk = Disk('./vDisks/myDisk.adrv', 4 * 1000 ** 3) # Create a 4GB disk.
myDisk.delete('/hello/world.txt') # Similary to write(), you can get the amount of bytes removed from the disk
```

**Disk.delete() - Parameters:**
> `vpath: str` - Path of the file to deleted

## 5- Formatting and file system informations

### Formatting the disk