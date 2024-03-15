class BaseHandlerException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CommandException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)