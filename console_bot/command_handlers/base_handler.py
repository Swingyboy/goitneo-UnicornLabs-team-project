from abc import ABC, abstractmethod


class BaseCommandHandler(ABC):
    """Base class for command handlers."""

    def __init__(self, bot: "ConsoleBot") -> None:
        self.bot = bot
        self.SUPPORTED_COMMANDS = {"add": self._add,
                                   "close": self._exit_bot,
                                   "delete": self._delete,
                                   "exit": self._exit_bot,
                                   "get": self._get,
                                   "get-all": self._get_all,
                                   "help": self._get_help,
                                   "hello": self._hello_bot,
                                   "update": self._update,




                                   }

    @abstractmethod
    def _add(self, *args) -> None:
        ...

    @abstractmethod
    def _get(self, *args) -> str:
        ...

    @abstractmethod
    def _get_all(self, *args) -> str:
        ...

    @abstractmethod
    def _update(self) -> None:
        ...

    @abstractmethod
    def _delete(self) -> None:
        ...

    @abstractmethod
    def _get_help(self) -> str:
        ...

    @abstractmethod
    def _exit_bot(self) -> str:
        ...

    @abstractmethod
    def _hello_bot(self) -> str:
        ...
