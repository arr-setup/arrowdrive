import io
import os
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

    def __read(self, _path: str, encoding: str | None = None) -> str:
         with open(self.path, 'rb') as _file:
            archive = io.BytesIO(_file.read())

            with zipfile.ZipFile(archive, 'r') as zip_buffer:
                try:
                    content = zip_buffer.read(_path)
                    if encoding is None:
                        return content
                    else:
                        return content.decode(encoding)

                except:
                    raise FileNotFoundError(f"{_path} was not found.")
                    
    def __write(self, content: str | bytes, _path: str) -> int:
        if self.size.raw + len(content) > self.max_size.raw:
            raise FullDiskError(f'Could not write anything at {_path} as its content would overload the disk. Available space: {Size(self.max_size.raw - self.size.raw).literal()} / File size: {len(content)}')
        else:
            with zipfile.ZipFile(self.path, 'a') as zip_buffer:
                zip_buffer.writestr(_path, content)
            
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

    def __sys_data(self, _name: str, _data: str = '', _mode: str = 'r') -> list[str] | None:
        _path = os.path.join('/.sys/', _name)
        if _mode == 'r':
            return self.__read(_path, 'UTF-8').split('\n')
        elif _mode == 'w':
            self.__write(_data.decode(), _path)
        elif _mode == 'a':
            data = self.__read(_path, 'UTF-8')
            _data = '\n'.join((data, _data.decode()))
            self.__delete(_path)
            self.__write(_data, _path)

    def __ls(self) -> list[str]:
        with zipfile.ZipFile(self.path, 'r') as zip_buffer:
            return zip_buffer.namelist()
    
    """
    Main Disk methods
    """

    def format_disk(self):
        """
        Empty a Disk, repair a damaged Disk or format any file to make it usable by ADRV.
        No params, returns None
        """

        # Reset the disk
        blank = io.BytesIO()
        with open(self.path, 'wb') as buffer:
            buffer.write(blank.getvalue())
        
        # Create system files
        self.__sys_data('Disk/$Registry', _mode = 'w')
        self.__sys_data('Disk/$Properties', f'{self.name}\n{self.max_size.raw}\n{round(time.time())}\n{VERSION}\n{SUPPORTS}', 'w')

        # Tests :
        name = self.__sys_data('Disk/$Properties')[0]
        if name != self.name:
            raise BrokenDiskError('Something went wrong while formatting your disk.')

        if len(self.__ls()) != 2:
            raise BrokenDiskError('Something went wrong while formatting your disk.')
        
        print('Formatting done')
        
    def write(self, vPath: str, content: str | bytes = '', mode: str = 'a') -> int:
        """
        Write a file to Disk.\n

        - Params:\n
            vPath: file destination path\n
            Mode 'a': append or edit a file\n
                 'w': create or replace a file\n
        - Returns: weigth of added content, in bytes
        """

        if mode == 'w':
            _file = { 'path': vPath, 'address': str(uuid.uuid4()), 'timestamp': round(time.time()) }
            self.__delete(_file['address'])
            self.__write(content, _file['address'])
            self.__sys_data('Disk/$Registry', '::'.join(map(str, _file.values())), _mode='a')
        elif mode == 'a':
            registry = self.__sys_data('Disk/$Registry')
            try: _file = [ _item for _item in registry if _item.split('::')[0] == vPath ][0].split('::')
            except IndexError:
                self.write(vPath, content, mode = 'w')
                return

            _file = dict(zip([ 'path', 'address', 'timestamp' ], _file))

            data = self.__read(_file['address'])
            _data = '\n'.join((str(data), str(content)))

            self.__delete(_file['address'])
            self.__write(_data, _file['address'])

        return len(content)

    def read(self, vPath: str) -> FileResponse:
        """
        Get a file, its contents and some information.\n

        - Params:\n
            vPath: path of the file to be read\n
        - Returns: FileResponse
        """

        registry = self.__sys_data('Disk/$Registry')
        try: _file = [ _item for _item in registry if _item.split('::')[0] == vPath ][0].split('::')
        except KeyError: raise FileNotFoundError(f"'{vPath}' doesn't exist.")
        
        data = self.__read(f'/{_file[1]}')
        return FileResponse(data, _file[2])
    
    def delete(self, vPath: str) -> int:
        """
        Remove a file from a disk\n

        - Params:\n
            vPath: path of the file to be deleted\n
        - Returns: weight of deleted content, in bytes
        """

        registry = self.__sys_data('Disk/$Registry')
        try: _file = [ _item for _item in registry if _item.split('::')[0] == vPath ][0].split('::')
        except KeyError: raise FileNotFoundError(f"'{vPath}' doesn't exist.")
        
        data = self.__read(f'/{_file[1]}')
        return FileResponse(data, _file[2])
