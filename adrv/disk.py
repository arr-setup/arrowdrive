import io
import os
import tempfile
import zipfile

from ._cls import *
from .utils import *

class Disk:
    def __init__(self, name: str = 'vDisk', path: str = './', max_size: int = 1000 ** 2):
        self.name = name
        self.path = f"{path}/{name}.adrv".replace('//', '/')
        self.max_size = Size(max_size)
        self.size = Size(0)

        try:
            with open(self.path, 'rb') as file:
                for block in file:
                    if block[0] != b'\0':
                        raise ValueError("File is not bytes")
        except:
            _dirs = self.path.split('/')
            _dirs.pop()
            _dirs = '/'.join(_dirs)
            if not os.path.exists(_dirs):
                print(self.path)
                os.makedirs(_dirs)
                
            with open(self.path, 'wb') as file:
                pass

    def open_file(self, vPath: str) -> FileResponse:
         with open(self.path, 'rb') as file:
            archive = io.BytesIO(file.read())

            with zipfile.ZipFile(archive, 'r') as zip_buffer:
                with tempfile.TemporaryDirectory() as tempDir:
                    zip_buffer.extractall(tempDir)
                    vPath = os.path.normpath(vPath)
                    tempPath = os.path.normpath(f"{tempDir}/{vPath}")

                    if os.path.exists(tempPath):
                        if os.path.isdir(tempPath):
                            raise FileIsDirectoryError(f"{vPath} is a directory.")
                        else:
                            with open(tempPath, 'rb', encoding = None) as extracted_file:
                                content = extracted_file.read()
                                
                            return FileResponse(content, vPath, os.path.getmtime(tempPath))
                    else:
                        raise FileNotFoundError(f"{vPath} was not found.")
                    
    def write(self, content: str | bytes, vPath: str, name: str) -> int:
        if self.size.raw + len(content) > self.max_size.raw:
            raise FullDiskError(f'Could not write anything at {vPath} as its content would overload the disk. Available space: {Size(self.max_size.raw - self.size.raw).literal()} / File size: {len(content)}')
        else:
            with zipfile.ZipFile(self.path, 'a') as archive:
                os.makedirs(f"./temp/{vPath}")
                filePath = os.path.normpath(f"{vPath}/{name}")
                with open(f"./temp/{filePath}", 'w' if type(content) == str else 'wb') as file:
                    file.write(content)
            
                archive.write(f"./temp/{filePath}", filePath)
                os.remove(f"./temp/{filePath}")
                os.removedirs(f"./temp/{vPath}")
            
            self.size.raw += len(content)
            return len(content)
    
    def remove(self, vPath: str):
        vPath = os.path.normpath(vPath)

        try:
            _file = self.open_file(vPath)
        except FileNotFoundError:
            return 0
        
        self.size.raw -= _file.size

        with open(self.path, 'rb') as file:
            archive = io.BytesIO(file.read())

        with zipfile.ZipFile(archive, 'r') as zip_buffer:
            new_archive = io.BytesIO()
            with zipfile.ZipFile(new_archive, 'a', zipfile.ZIP_DEFLATED) as new_zip:
                for file_info in zip_buffer.infolist():
                    if file_info.filename != vPath:
                        content = zip_buffer.read(file_info.filename)
                        new_zip.writestr(file_info, content)

        with open(self.path, 'wb') as file:
            file.write(new_archive.getvalue())

        return _file.size