# ArrowDrive-Reader
Special reader for ArrowBit virtual disks.
vDisk extension: `.adrv`

## How to use it

```py
import adrv
```

### Create a Disk object

```py
myDisk = adrv.Disk('./vDisks/myDisk.adrv', 4 * 1000 ** 3) # Create a 4GB disk.
```

You just created a new Disk object that points to the given path. If the disk doesn't exist, it will be created with the necessary directories.