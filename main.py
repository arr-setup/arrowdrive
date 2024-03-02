import os

from adrv.disk import Disk, Size, convert
from adrv.bridge import *

disk = Disk('example', '.', convert(4, 'GB', 'B')) # Creates a 4GB virtual disk
bridge = PhysicalBridge(disk) # Setup the bridge to the wanted disk

bridge.copy('README.md', '/repo', 'README') # Copy a real file to the virtual disk.
bridge.copy('LICENSE', '/repo') # The third parameter specifies the name of the virtual file, and it's optional
amount_written = bridge.copy('./adrv/disk.py', '/scripts', 'main.py') # And you can collect the amount of bytes written on the disk.

print(f"{Size(amount_written).literal()} have been written.")

percentageUsed = round(disk.size.raw / disk.max_size.raw * 10000) / 100
print(f"{'None' if percentageUsed == 0 else f'{percentageUsed}%'} of the storage used ({disk.size.literal()} out of {disk.max_size.literal()})")


try:
	os.makedirs('dist/')
except:
	pass


bridge.extract('/repo/LICENSE', 'dist/LICENSE')
content = bridge.extract('/repo/README', 'dist/README.md').content # The extract() method also returns a FileResponse

disk.remove('/repo/LICENSE') # You can remove files easily
amount_deleted = disk.remove('/repo/README') # And get the amount of bytes deleted as well

percentageUsed = round(disk.size.raw / disk.max_size.raw * 10000) / 100
print(f"{'None' if percentageUsed == 0 else f'{percentageUsed}%'} of the storage used ({disk.size.literal()} out of {disk.max_size.literal()})")