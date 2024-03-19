class FileResponse:
    def __init__(self, content: bytes, name: str, timestamp: float) -> None:
        """
        The response you get when you have opened a file successfully.\n

        Attributes:\n
        .content - The file content (bytes)\n
        .name - The file name with the extension\n
        .timestamp - The file creation timestamp\n
        .size - The file size in bytes\n
        """

        self.content = content
        self.name = name
        self.timestamp = timestamp
        self.size = len(content)

class DiagnoseResponse:
    def __init__(self):
        self.disk_format = False
        self.is_supported = False
        self.primary_files = False
    
    def result(self) -> bool:
        if not self.disk_format: return False
        if not self.is_supported: return False
        if not self.primary_files: return False

        return True

# Errors

class FullDiskError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class BrokenDiskError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__('The disk appears to be broken. Try using disk.extract_all() to get back some data, or format the disk with disk.format_disk().')

class FileIsDirectoryError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)