from adrv.disk import Disk, Size, convert
from adrv.bridge import *

disk = Disk('example', './dist', convert(4, 'GB', 'B'))
disk.format_disk()

try:
    disk.write('/hello/world.txt', 'Hello world!', 'w')
    print(disk.read('/hello/world.txt').content)
except Exception as e:
    print(e)
    disk.extract_all('./dist')

print(disk.f_list())
print(disk.f_list(include_ts = True))