class FileExtensionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SaveAsError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
