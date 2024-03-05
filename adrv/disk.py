import io
import json
import os
import tempfile
import time
import uuid
import zipfile

from ._cls import *
from .utils import *

VERSION = "0.2"
SUPPORTS = "0.2"

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
            if not os.path.exists(path):
                try: os.makedirs(path)
                except: pass
                
            with open(self.path, 'wb') as file:
                self.format_disk()

    def __read(self, _path: str) -> str:
         with open(self.path, 'rb') as file:
            archive = io.BytesIO(file.read())

            with zipfile.ZipFile(archive, 'r') as zip_buffer:
                with tempfile.TemporaryDirectory() as tempDir:
                    zip_buffer.extractall(tempDir)
                    _path = os.path.normpath(_path)
                    tempPath = os.path.normpath(os.path.join(tempDir, _path))

                    if os.path.exists(tempPath):
                        if os.path.isdir(tempPath):
                            raise FileIsDirectoryError(f"{_path} is a directory.")
                        else:
                            with open(tempPath, 'rb') as extracted_file:
                                content = extracted_file.read().decode('UTF-8')
                                
                            return content
                    else:
                        raise FileNotFoundError(f"{_path} was not found.")
                    
    def __write(self, content: str | bytes, _path: str) -> int:
        # name = _path.split('/')[-1]
        # _dirs = '/'.join(_path.split('/')[0 : -2])
        # _path = os.path.normpath(_dirs).replace('\\', '/')

        if self.size.raw + len(content) > self.max_size.raw:
            raise FullDiskError(f'Could not write anything at {_path} as its content would overload the disk. Available space: {Size(self.max_size.raw - self.size.raw).literal()} / File size: {len(content)}')
        else:
            with zipfile.ZipFile(self.path, 'a') as zip_buffer, tempfile.TemporaryDirectory(dir = '.') as tempDir:
                zip_buffer.writestr(_path, content)
                filePath: str
                
                """
                if _path[0] in ['/', '\\']:
                    os.makedirs(os.path.join(tempDir, _path[1:]))
                else:
                    print(_path)
                    os.makedirs(os.path.join(tempDir, _path))

                # filePath = os.path.join(_path, name)

                with open(os.path.join(tempDir, filePath), 'w' if type(content) == str else 'wb') as _file:
                    _file.write(content)
            
                zip_buffer.write(os.path.join(tempDir, filePath), filePath)
                """
            
            self.size.raw += len(content)
            return len(content)
    
    def __delete(self, _path: str):
        try:
            _file = self.__read(_path)
            self.size.raw -= len(_file)
        except FileNotFoundError:
            return 0
        
        new_archive = io.BytesIO()
        with zipfile.ZipFile(self.path, 'r') as zip_buffer, zipfile.ZipFile(new_archive, 'a', zipfile.ZIP_DEFLATED) as new_zip:
            for file_info in zip_buffer.infolist():
                if file_info.filename != _path:
                    content = zip_buffer.read(file_info.filename)
                    new_zip.writestr(file_info, content)

            with open(self.path, 'wb') as buffer:
                buffer.write(new_archive.getvalue())

        return len(_file)

    def __edit_sys(self, _name: str, _data: str = '', _mode: str = 'r') -> str | None:
        _path = os.path.join('/.sys/', _name)
        if _mode == 'r':
            return self.__read(_path).split('\n')
        elif _mode == 'w':
            self.__write(_data, _path)
        elif _mode == 'a':
            print(_data)
            data = self.__read(_path)
            _data = '\n'.join((str(data), str(_data)))
            self.__delete(_path)
            self.__write(_data, _path)
    
    """
    Main Disk functions
    """

    def format_disk(self):
        # Reset the disk
        blank = io.BytesIO()
        with open(self.path, 'wb') as buffer:
            buffer.write(blank.getvalue())
        
        # Create system files
        self.__edit_sys('Disk/$Registry', '', 'w')
        self.__edit_sys('Disk/$Properties', f'{self.name}\n{self.max_size.raw}\n{round(time.time())}\n{VERSION}\n{SUPPORTS}', 'w')

    def write(self, vPath: str, content: str | bytes = '', mode: str = 'a') -> int:
        if mode == 'w':
            _file = { 'path': vPath, 'address': str(uuid.uuid4()), 'timestamp': round(time.time()) }
            self.__delete(_file['address'])
            self.__write(content, _file['address'])
            self.__edit_sys('Disk/$Registry', '::'.join(map(str, _file.values())), _mode='a')
        elif mode == 'a':
            registry = self.__edit_sys('Disk/$Registry')
            try: _address = [ _item for _item in registry if _item.split('::')[0] == vPath ][0]
            except IndexError:
                self.write(vPath, content, mode = 'w')
                return

            _file = dict(zip([ 'path', 'address', 'timestamp' ], _address.split('::')))

            data = self.__read(_file['address'])
            _data = '\n'.join((str(data), str(content)))

            self.__delete(_file['address'])
            self.__write(_data, _file['address'])

        return len(content)

    def read(self, vPath: str) -> FileResponse:
        registry = self.__edit_sys('Disk/$Registry')
        try: _address = [ _item for _item in registry if _item.split('::')[0] == vPath ][0]
        except IndexError:
            print(vPath)
            print([ _item.split('::')[0] for _item in registry ], vPath)
            raise FileNotFoundError(f"'{vPath}' doesn't exist.")
        
        _file = dict(zip([ 'path', 'address', 'timestamp' ], _address.split('::')))

        data = self.__read(_file['address'])
        return data