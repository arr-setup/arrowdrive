import io
import os
import shutil
import tempfile
import time
import uuid
import zipfile

from ._cls import *
from .utils import *

VERSION = "1.1.0"
SUPPORTS = "1.0.0"

class Disk:
    def __init__(self, name: str = 'vDisk', path: str = './', max_size: int = 1000 ** 2):
        """
        Initializes a Disk instance.

        Args:
            name (str, optional): The name of the disk. Defaults to 'vDisk'.
            path (str, optional): The path where the disk will be stored. Defaults to './'.
            max_size (int, optional): The maximum size of the disk in bytes. Defaults to 1000000.
        """
        self.name = name.upper()
        self.path = os.path.join(path, f"{name}.adrv")
        self.max_size = Size(max_size)
        self.size = Size(0)

        if not zipfile.is_zipfile(self.path):
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except:
                    pass
                
            self.format_disk()
        
        if not self.diagnosis(True).primary_files:
            self.format_disk()
        
        properties = self.__sys_data('Disk/$Properties')
        self.name = properties[0]
        self.max_size = Size(int(properties[1]))
        self.size = Size(os.path.getsize(self.path))

    def __read(self, _path: str, encoding: str | None = 'UTF-8') -> str:
        """
        Reads content from a file in the disk.

        Args:
            _path (str): The path of the file to be read.
            encoding (str | None, optional): The encoding of the file. Defaults to 'UTF-8'.

        Returns:
            str: The content of the file.
        """
        with open(self.path, 'rb') as _file:
            archive = io.BytesIO(_file.read())

            with zipfile.ZipFile(archive, 'r') as zip_buffer:
                with tempfile.TemporaryDirectory() as tempDir:
                    zip_buffer.extractall(tempDir)
                    vPath = os.path.normpath(_path)
                    tempPath = os.path.normpath(f"{tempDir}/{vPath}")

                    if os.path.exists(tempPath):
                        if os.path.isdir(tempPath):
                            raise FileIsDirectoryError(f"{vPath} is a directory.")
                        else:
                            with open(tempPath, 'rb', encoding = None) as extracted_file:
                                content = extracted_file.read()
                                
                            return content.decode(encoding)
                    else:
                        raise FileNotFoundError(f"{vPath} was not found.")
                    
    def __write(self, content: str | bytes, _path: str) -> int:
        """
        Writes content to a file in the disk.

        Args:
            content (str | bytes): The content to be written.
            _path (str): The path where the content will be written.

        Returns:
            int: The size of the content written.
        """
        if self.size.raw + len(content) > self.max_size.raw:
            raise FullDiskError(f'Could not write anything at {_path} as its content would overload the disk. Available space: {Size(self.max_size.raw - self.size.raw).literal()} / File size: {len(content)}')
        
        with zipfile.ZipFile(self.path, 'a') as archive:
            with tempfile.TemporaryDirectory() as tempDir:
                filePath = os.path.normpath(f"{tempDir}/cachedfile")
                with open(filePath, 'w' if isinstance(content, str) else 'wb') as _file:
                    _file.write(content)
                
                archive.write(filePath, _path)

        self.size.raw += len(content)
        return len(content)
    
    def __delete(self, _path: str):
        """
        Deletes a file from the disk.

        Args:
            _path (str): The path of the file to be deleted.

        Returns:
            int: The size of the deleted file.
        """
        try:
            _file = self.__read(_path)
            self.size.raw -= len(_file)
        except FileNotFoundError:
            return 0
        
        with tempfile.TemporaryDirectory() as tempDir, tempfile.TemporaryDirectory() as tempCache, zipfile.ZipFile(self.path, 'r') as old_archive:
            # Re-write without the file
            old_archive.extractall(tempDir)

            try:
                os.remove(os.path.join(tempDir, _path))
            except:
                return 0

            # Compression
            _cachePath = shutil.make_archive(os.path.join(tempCache, 'cachedArchive'), 'zip', tempDir)
            with open(_cachePath, 'rb') as _cache, open(self.path, 'wb') as _archive:
                _archive.write(_cache.read())

        return len(_file)

    def __sys_data(self, _name: str, _data: str = '', _mode: str = 'r') -> list[str] | None:
        """
        Handles system data operations.

        Args:
            _name (str): The name of the system data.
            _data (str, optional): The data to be written. Defaults to ''.
            _mode (str, optional): The mode of operation ('r', 'w', 'a'). Defaults to 'r'.

        Returns:
            list[str] | None: The system data.
        """
        _path = os.path.join('/.sys/', _name)
        if _mode == 'r':
            return self.__read(_path, 'UTF-8').replace('\r', '').split('\n')
        elif _mode == 'w':
            self.__write(_data, _path)
        elif _mode == 'a':
            data = self.__read(_path, 'UTF-8')
            if data != '':
                _data = '\n'.join((data, _data))
            
            self.__write(_data, _path)

    def __ls(self) -> list[str]:
        """
        Lists files in the disk.

        Returns:
            list[str]: The list of files in the disk.
        """
        with zipfile.ZipFile(self.path, 'r') as zip_buffer:
            return list(set(zip_buffer.namelist()))
    
    def format_disk(self, modelPath: str | None = None):
        """
        Formats the disk.
        """

        blank = io.BytesIO()
        with open(self.path, 'wb') as buffer:
            buffer.write(blank.getvalue())
        
        self.__sys_data('Disk/$Registry', _mode = 'w')
        self.__sys_data('Disk/$Properties', f'{self.name.upper()}\n{self.max_size.raw}\n{round(time.time())}\n{VERSION}', 'w')
        
        if modelPath is not None:
            with zipfile.ZipFile(modelPath, 'r') as archive:
                try:
                    if '.sys/Disk/$Registry' in archive.namelist():
                        namelist = [ { "path": item.split('::')[1], "vPath": item.split('::')[0] } for item in archive.read('.sys/Disk/$Registry').decode().split('\n') ]
                    else:
                        namelist = [ { "path": path, "vPath": path } for path in archive.namelist() if not path.startswith('.sys') ]
                except IndexError:
                    namelist = [ { "path": path, "vPath": path } for path in archive.namelist() if not path.startswith('.sys') ]
                
                for name in namelist:
                    content = archive.read(name['path'])
                    self.write(name['vPath'], content, 'w')
        
        if not self.diagnosis(snooze = True):
            self.extract_all('./.local')
            raise BrokenDiskError("Something went wrong while formatting your disk. It has automatically been extracted in .local")    

    def extract_all(self, target: str) -> None:
        """
        Extracts all files from the disk to a target directory.

        Args:
            target (str): The target directory.
        """
        with zipfile.ZipFile(self.path) as zip_buffer:
            zip_buffer.extractall(target)
    
    def f_list(self, include_ts: bool = False, sys = False) -> list[str | dict]:
        """
        Lists files in the disk.

        Args:
            include_ts (bool, optional): Whether to include timestamps. Defaults to False.

        Returns:
            list[str | dict]: The list of files in the disk.
        """

        registry = self.__sys_data('Disk/$Registry')
        namelist = []

        for _item in registry:
            if _item == '':
                continue

            if include_ts:
                namelist.append({ 'path': _item.split('::')[0], 'timestamp': _item.split('::')[2] })
            else:
                namelist.append(_item.split('::')[0])
        
        if sys:
            print(self.__ls())
            for name in self.__ls():
                if name.startswith('.sys/') and not name.endswith('/'):
                    if include_ts:
                        namelist.append({'path': name, 'timestamp': 0 })
                    else:
                        namelist.append(name)
        
        return namelist

    def diagnosis(self, snooze: bool = False) -> DiagnoseResponse:
        """
        Evaluates the health of the disk.

        Args:
            snooze (bool, optional): Whether to suppress output. Defaults to False.

        Returns:
            bool: True if the disk is healthy, False otherwise.
        """

        if not snooze:
            print("Evaluating health of your disk...")

        status = {}

        if not zipfile.is_zipfile(self.path):
            status["DataFormat"] = "\033[31;40mIncorrect\033[0m"
        else:
            status["DataFormat"] = "\033[32;40mCorrect\033[0m"

        try:
            last_v = self.__sys_data('Disk/$Properties')[3]
            if last_v.split('.')[0] < VERSION.split('.')[0] or (last_v.split('.')[0] == VERSION.split('.')[0] and last_v.split('.')[1] < VERSION.split('.')[1]):
                status["DiskVersion"] = f"\033[31;40mUnsupported\033[0m ({last_v} | Required: {SUPPORTS})"
            else:
                status["DiskVersion"] = "\033[32;40mSupported\033[0m"
        except:
            status["DiskVersion"] = "\033[31;40mUnknown\033[0m"

        try:
            for _name in ['$Registry', '$Properties']:
                if f".sys/Disk/{_name}" not in self.__ls():
                    status["PrimaryFiles"] = "\033[31;40mMissing\033[0m"
                    break
            else:
                status["PrimaryFiles"] = "\033[32;40mPresent\033[0m"
        except:
            status["PrimaryFiles"] = "\033[31;40mMissing\033[0m"

        if not snooze:
            for section, result in status.items():
                print(section, ": ", result, sep="")

        response = DiagnoseResponse()
        response.disk_format = 'Incorrect' not in status['DataFormat']
        response.is_supported = 'Un' not in status['DiskVersion']  # UN-known and UN-supported return False
        response.primary_files = 'Present' in status['PrimaryFiles']

        return response


    def write(self, vPath: str, content: str | bytes = '', mode: str = 'a') -> int:
        """
        Writes content to a file in the disk.

        Args:
            vPath (str): The path where the content will be written.
            content (str | bytes, optional): The content to be written. Defaults to ''.
            mode (str, optional): The writing mode ('a', 'w'). Defaults to 'a'.

        Returns:
            int: The size of the content written.
        """
        if mode == 'w':
            _file = { 'path': vPath, 'address': str(uuid.uuid4()), 'timestamp': round(time.time()) }
            self.__delete(_file['address'])
            self.__write(content, _file['address'])
            self.__sys_data('Disk/$Registry', '::'.join(map(str, _file.values())), _mode = 'a')
        elif mode == 'a':
            registry = self.__sys_data('Disk/$Registry')
            try:
                _file = [ _item for _item in registry if _item.split('::')[0] == vPath ][0].split('::')
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
        Reads a file from the disk.

        Args:
            vPath (str): The path of the file to be read.

        Returns:
            FileResponse: The response containing the file data.
        """
        registry = reversed(self.__sys_data('Disk/$Registry'))
        try:
            _file = [ _item for _item in registry if _item.split('::')[0] == vPath ][0].split('::')
        except IndexError:
            raise FileNotFoundError(f"'{vPath}' doesn't exist.")
        
        data = self.__read(f'/{_file[1]}')
        return FileResponse(data, os.path.basename(_file[1]), _file[2])
    
    def delete(self, vPath: str) -> int:
        """
        Deletes a file from the disk.

        Args:
            vPath (str): The path of the file to be deleted.

        Returns:
            int: The size of the deleted file.
        """

        registry = self.__sys_data('Disk/$Registry')
        try:
            _file = [ _item for _item in registry if _item.split('::')[0] == vPath ][0].split('::')
            new_registry = '\n'.join([ _item for _item in registry if _item.split('::')[0] != vPath and _item != '' ])
        except KeyError:
            raise FileNotFoundError(f"'{vPath}' doesn't exist.")
        
        data = self.__read(f'/{_file[1]}')
        self.__delete(_file[1])
        self.__sys_data('Disk/$Registry',_data = new_registry, _mode = 'w')
        return len(data)
