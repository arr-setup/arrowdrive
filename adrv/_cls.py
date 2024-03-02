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

# Errors

class FullDiskError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class FileIsDirectoryError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)