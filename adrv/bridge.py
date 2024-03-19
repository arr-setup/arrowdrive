import os

from . import Disk
from ._cls import *

class PhysicalBridge:
    def __init__(self, disk: Disk):
        self.disk = disk

    def bring(self, vPath: str, newPath: str):
        try:
            directories: list = tuple(newPath.split('/')[ : -2 ])
            if len(directories) >= 2:
                os.makedirs(os.path.join(directories[0], *directories[ 1 : ]))
        except FileExistsError: pass
        
        with open(newPath, 'wb') as _file:
            _file.write(self.disk.read(vPath).content)

        return self.disk.read(vPath)

    def send(self, filePath: str, vPath: str):
        with open(filePath, 'rb') as _file:
            amount_written = self.disk.write(vPath, _file.read(), 'w')

        return amount_written

class VirtualBridge:
    def __init__(self, firstDisk: Disk, secondDisk: Disk):
        self.left = firstDisk
        self.right = secondDisk
    
    def cross(self, targetPath: str, finalPath: str = '/shore', rtl: bool = False):
        if rtl:
            sender, receiver = self.right, self.self
        else:
            sender, receiver = self.left, self.right

        _pkg = sender.read(targetPath)
        receiver.write(_pkg.content, finalPath, _pkg.name)