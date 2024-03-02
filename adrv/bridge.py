import os

from .disk import Disk
from ._cls import *

class PhysicalBridge:
    def __init__(self, disk: Disk = Disk()):
        self.disk = disk

    def save_from_vdisk(self, vPath: str, newPath: str):
        try:
            directories: list = newPath.split('/')
            directories = directories.pop()
            os.makedirs('/'.join(directories))
        except FileExistsError:
            pass
        
        with open(newPath, 'wb') as _file:
            _file.write(self.disk.open_file(vPath).content)

        return self.disk.open_file(vPath)

    def copy(self, vPath: str, filePath: str, name: str):
        with open(vPath, 'rb') as _file:
            amount_written = self.disk.write(_file.read(), filePath, name)

        return amount_written