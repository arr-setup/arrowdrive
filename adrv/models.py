class FileResponse:
    def __init__(self, content: bytes, name: str, timestamp: float) -> None:
        """
        The response you get when you have opened a file successfully.

        Args:
            content (bytes): The file content
            name (str): The file name with the extension
            timestamp (float): The file creation timestamp
            size (int): The file size in bytes
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