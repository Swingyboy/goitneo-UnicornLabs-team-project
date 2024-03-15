class AddressBookException(Exception):
    """A class to represent an address book exception."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoteBookException(Exception):
    """A class to represent a note book exception."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
