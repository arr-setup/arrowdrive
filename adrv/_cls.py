class FileResponse:
    def __init__(self, content: str, name: str, timestamp: float) -> None:
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