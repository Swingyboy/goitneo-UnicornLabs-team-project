from abc import ABC, abstractmethod


class BaseCommandHandler(ABC):
    def __init__(self, bot: "ConsoleBot") -> None:
        self.bot = bot
        self.SUPPORTED_COMMANDS = {"add": self._add_contact,
                                   "add-birthday": self._add_birthday,
                                   "all": self._get_all,
                                   "birthdays": self._get_birthdays_per_week,
                                   "change": self._change_contact,
                                   "close": self._exit_bot,
                                   "exit": self._exit_bot,
                                   "hello": self._hello_bot,
                                   "help": self._get_help,
                                   "phone": self._get_phone,
                                   "show-birthday": self._show_birthday
                                   }

    @abstractmethod
    def _add_contact(self, *args) -> str:
        ...

    @abstractmethod
    def _change_contact(self, *args) -> str:
        ...

    @abstractmethod
    def _get_all(self) -> None:
        ...

    @abstractmethod
    def _get_help(self) -> str:
        ...

    @abstractmethod
    def _get_phone(self, *args) -> str:
        ...

    @abstractmethod
    def _add_birthday(self, *args) -> str:
        ...

    @abstractmethod
    def _show_birthday(self, *args) -> str:
        ...

    @abstractmethod
    def _get_birthdays_per_week(self) -> None:
        ...

    @abstractmethod
    def _exit_bot(self) -> str:
        ...

    @abstractmethod
    def _hello_bot(self) -> str:
        ...
