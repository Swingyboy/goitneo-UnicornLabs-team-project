from typing import Dict, Union

from contacts import Record
from base_handler import BaseCommandHandler


def input_error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError as a_ex:
            if func.__name__ == "_show_birthday":
                return "Birthday for this contact was not specified."
            else:
                return str(a_ex)
        except ValueError as v_ex:
            if func.__name__ == "_add_contact":
                return ("Invalid number of arguments for add command, please try again. "
                        "Give at least a name and a phone number, please.")
            elif func.__name__ == "_change_contact":
                return ("Invalid number of arguments for change command, please try again."
                        " Give me name, old phone and new phone numbers please.")
            elif func.__name__ == "_get_phone":
                return "Invalid number of arguments for phone command, please try again. Give me name please."
            elif func.__name__ == "_add_birthday":
                return ("Invalid number of arguments for add-birthday command, "
                        "please try again. Give me name and birthday please.")
            else:
                return str(v_ex)
        except IndexError as i_ex:
            if func.__name__ == "_add_contact":
                return ("Invalid number of arguments for add command, please try again.\n"
                        "Give me name and phone please. Also email and address are optional.")
            if func.__name__ == "_get_phone":
                return "Invalid number of arguments for phone command, please try again. Give me name please."
            else:
                return str(i_ex)

    return inner


class DefaultCommandHandler(BaseCommandHandler):
    def __init__(self, bot: "ConsoleBot") -> None:
        super().__init__(bot)
        self.bot = bot
        self.SUPPORTED_COMMANDS.update({"add-address": self._add_address,
                                        "add-email": self._add_email,
                                        "add-note": self._add_note,
                                        "delete": self._delete_contact,
                                        "get-notes": self._get_notes,
                                        "remove": self._delete_contact,
                                        "search": self._find_contact,
                                        "search-note": self._find_note,
                                        }
                                       )

    @input_error_handler
    def _add_birthday(self, *args) -> str:
        name, birthday = args
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            result.add_birthday(birthday)
            return f"Birthday for {name.capitalize()} has been added."
        return result

    @input_error_handler
    def _add_contact(self, *args) -> str:
        name, *user_data = args
        if self.bot.address_book.find(name):
            change = input(f"Contact {name.capitalize()} already exists. Do you want to change it?")
            if change.lower() in ["yes", "y"]:
                return self._change_contact(*args)
            else:
                self._hello_bot()
        else:
            record = Record.from_tuple(name, *user_data)
            self.bot.address_book.add_record(record)
            return f"Contact {name.capitalize()} has been added."

    @input_error_handler
    def _add_email(self, *args) -> str:
        name, email = args
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            result.add_email(email)
            return f"Email for {name.capitalize()} has been added."
        return result

    @input_error_handler
    def _add_address(self, *args) -> str:
        name, address = args
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            result.add_address(address)
            return f"Address for {name.capitalize()} has been added."
        return result

    @input_error_handler
    def _add_note(self, *args) -> str:
        self.bot.note_book.new_note(*args)
        return "Note has been added."

    @input_error_handler
    def _change_contact(self, *args) -> str:
        name, *user_data = args
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            result.update_fields_from_tuple(*user_data)
            return f"Contact {name.capitalize()} was updated."
        return result

    @input_error_handler
    def _check_contact_exist(self, name: str) -> Union[Record, str]:
        record = self.bot.address_book.find(name)
        if not record:
            return f"Contact {name.capitalize()} does not exist."
        else:
            return record

    @input_error_handler
    def _delete_contact(self, *args) -> str:
        name = args[0]
        result = self.bot.address_book.delete(name)
        if result:
            return f"Contact {name.capitalize()} has been deleted."
        return f"Contact {name.capitalize()} does not exist."

    @input_error_handler
    def _find_contact(self, by_field: str, value: str) -> str:
        result = self.bot.address_book.search(by_field, value)
        if result:
            return result
        return f"No contacts found with {by_field} {value}."

    @input_error_handler
    def _find_note(self, by_field: str, value: str) -> str:
        result = self.bot.note_book.search(by_field, value)
        if result:
            for note in result:
                print(f"Message: {note.text.value}\nTags: {', '.join([tag.value for tag in note.tags])}\n")
        return f"No notes found with {by_field} {value}."

    @input_error_handler
    def _get_all(self) -> None:
        for record in self.bot.address_book.get_all_records():
            res = f"{record.name.value.capitalize()}:\t{record.phone.value}"
            if record.email:
                res += f"\t{record.email.value}"
            if record.birthday:
                res += f"\t{record.birthday.value}"
            if record.address:
                res += f"\t{record.address.value}"
            print(res)

    def _get_help(self) -> str:
        return ("Supported commands:\n"
                "add <name> <phone> [birthday] [email] [address] - add a new contact\n"
                "add-birthday <name> <birthday> - add birthday to a contact\n"
                "add-email <name> <email> - add email to a contact\n"
                "add-address <name> <address> - add address to a contact\n"
                "all - show all contacts\n"
                "change <name> [new_phone] [new_birthday] [new_email] [new_address] - change contact\n"
                "delete <name> - delete contact\n"
                "exit, close - close the program\n"
                "hello - display welcome message\n"
                "phone <name> - show phone number\n"
                "show-birthday <name> - show birthday\n"
                "birthdays - show birthdays for the next 7 days\n"
                "help - show this message\n"
                )

    @input_error_handler
    def _get_notes(self):
        for note in self.bot.note_book.data:
            print(f"Message: {note.text.value}\nTags: {', '.join([tag.value for tag in note.tags])}\n")

    @input_error_handler
    def _get_phone(self, *args) -> str:
        name = args[0]
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            return f"{name.capitalize()}: {result.phone.value}"
        return result

    @input_error_handler
    def _show_birthday(self, *args) -> str:
        name = args[0]
        result = self.bot.address_book.find(name)
        if isinstance(result, Record):
            return f"{name.capitalize()}: {result.birthday.value}"
        return result

    @input_error_handler
    def _get_birthdays_per_week(self) -> None:
        self.bot.address_book.get_birthdays_per_week()

    def _exit_bot(self) -> str:
        return "Goodbye!"

    def _hello_bot(self) -> str:
        return "How can I help you?"
