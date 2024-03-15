class FieldException(Exception):
    """A class to represent a field exception."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoteException(Exception):
    """A class to represent a note exception."""
    def __init__(self, message: str) -> None:
        super().__init__(message)



class RecordException(Exception):
    """A class to represent a record exception."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
