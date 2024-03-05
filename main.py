from adrv.disk import Disk, Size, convert
from adrv.bridge import *

disk = Disk('example', './dist', convert(4, 'GB', 'B'))
disk.format_disk()

disk.write('/hey/hello.txt', 'zzz')
disk.read('/hey/hello.txt')