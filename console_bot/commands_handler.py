from contacts import Record


def input_error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as v_ex:
            if func.__name__ == "_add_contact":
                return "Invalid number of arguments for add command, please try again. Give me name and phone please."
            elif func.__name__ == "_change_contact":
                return ("Invalid number of arguments for change command, please try again."
                        " Give me name, old phone and new phone numbers please.")
            elif func.__name__ == "_get_phone":
                return "Invalid number of arguments for phone command, please try again. Give me name please."
            else:
                return str(v_ex)
        except IndexError as i_ex:
            if func.__name__ == "_get_phone":
                return "Invalid number of arguments for phone command, please try again. Give me name please."
            else:
                return str(i_ex)

    return inner


class DefaultCommandHandler:
    def __init__(self, bot: "ConsoleBot") -> None:
        self.book = bot.book
        self.SUPPORTED_COMMANDS = {"add": self._add_contact,
                                   "add-phone": self._add_phone,
                                   "add-birthday": self._add_birthday,
                                   "all": self._get_all,
                                   "change": self._change_contact,
                                   "close": self._exit_bot,
                                   "exit": self._exit_bot,
                                   "hello": self._hello_bot,
                                   "phone": self._get_phone,
                                   "show-birthday": self._show_birthday,
                                   "birthdays": self._get_birthdays_per_week,
                                   }

    @input_error_handler
    def _add_contact(self, *args) -> str:
        name, phone = args
        if self.book.find(name):
            change = input(f"Contact {name.capitalize()} already exists. Do you want to change it?")
            if change.lower() in ["yes", "y"]:
                return self._change_contact(name, phone)
            else:
                self._hello_bot()
        else:
            record = Record(name)
            record.add_phone(phone)
            self.book.add_record(record)
            return f"Contact {name.capitalize()} has been added."

    @input_error_handler
    def _add_phone(self, *args) -> str:
        name, phone = args
        record = self.book.find(name)
        if record:
            record.add_phone(phone)
            return f"Phone number {phone} has been added to contact {name.capitalize()}."
        else:
            return f"Contact {name.capitalize()} does not exist."

    @input_error_handler
    def _change_contact(self, *args) -> str:
        name, old_phone, new_phone = args
        record = self.book.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return f"Contact {name.capitalize()} has been updated."
        else:
            return f"Contact {name.capitalize()} does not exist."

    def _get_all(self) -> None:
        for record in self.book.get_all_records():
            print(f"{record.name.value.capitalize()}:\t{', '.join(phone.value for phone in record.phones)}")

    @input_error_handler
    def _get_phone(self, *args) -> str:
        name = args[0]
        record = self.book.find(name)
        if not record:
            return f"Contact {name.capitalize()} does not exist."
        else:
            return f"{name.capitalize()}: {', '.join(phone.value for phone in record.phones)}"

    @input_error_handler
    def _add_birthday(self, *args) -> str:
        name, birthday = args
        record = self.book.find(name)
        if not record:
            return f"Contact {name.capitalize()} does not exist."
        else:
            record.add_birthday(birthday)
            return f"Birthday for {name.capitalize()} has been added."

    @input_error_handler
    def _show_birthday(self, *args) -> str:
        name = args[0]
        record = self.book.find(name)
        if not record:
            return f"Contact {name.capitalize()} does not exist."
        else:
            return f"{name.capitalize()}: {record.birthday.value}"

    @input_error_handler
    def _get_birthdays_per_week(self) -> None:
        self.book.get_birthdays_per_week()

    def _exit_bot(self) -> str:
        return "Goodbye!"

    def _hello_bot(self) -> str:
        return "How can I help you?"
