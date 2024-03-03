import os

from .disk import Disk
from ._cls import *

class PhysicalBridge:
    def __init__(self, disk: Disk):
        self.disk = disk

    def extract(self, vPath: str, newPath: str):
        try:
            directories: list = newPath.split('/')
            directories.pop()
            os.makedirs('/'.join(directories))
        except FileExistsError:
            pass
        
        with open(newPath, 'wb') as _file:
            _file.write(self.disk.open_file(vPath).content)

        return self.disk.open_file(vPath)

    def copy(self, filePath: str, vPath: str, name: str = None):
        if name is None:
            name = filePath.split('/')[-1]

        with open(filePath, 'rb') as _file:
            amount_written = self.disk.write(_file.read(), vPath, name)

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

        _pkg = sender.open_file(targetPath)
        receiver.write(_pkg.content, finalPath, _pkg.name)