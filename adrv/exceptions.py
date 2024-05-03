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