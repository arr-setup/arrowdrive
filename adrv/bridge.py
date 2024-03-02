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