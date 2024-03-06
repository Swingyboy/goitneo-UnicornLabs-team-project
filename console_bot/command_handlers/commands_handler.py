from typing import Union

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
                return "Invalid number of arguments for add command, please try again. Give me name and phone please."
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
            if func.__name__ == "_get_phone":
                return "Invalid number of arguments for phone command, please try again. Give me name please."
            else:
                return str(i_ex)

    return inner


class DefaultCommandHandler(BaseCommandHandler):
    def __init__(self, bot: "ConsoleBot") -> None:
        super().__init__(bot)
        self.bot = bot
        self.SUPPORTED_COMMANDS.update({"add-phone": self._add_phone,
                                        "delete": self._delete_contact,
                                        "remove": self._delete_contact
                                        }
                                       )

    @input_error_handler
    def _add_contact(self, *args) -> str:
        name, phone = args
        if self.bot.book.find(name):
            change = input(f"Contact {name.capitalize()} already exists. Do you want to change it?")
            if change.lower() in ["yes", "y"]:
                return self._change_contact(name, phone)
            else:
                self._hello_bot()
        else:
            record = Record(name)
            record.add_phone(phone)
            self.bot.book.add_record(record)
            return f"Contact {name.capitalize()} has been added."

    @input_error_handler
    def _add_phone(self, *args) -> str:
        name, phone = args
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            result.add_phone(phone)
            return f"Phone number {phone} has been added to contact {name.capitalize()}."
        return result

    @input_error_handler
    def _change_contact(self, *args) -> str:
        name, old_phone, new_phone = args
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            result = result.edit_phone(old_phone, new_phone)
            if result:
                return f"Phone number {old_phone} has been changed to {new_phone} for contact {name.capitalize()}."
            else:
                return f"Phone number {old_phone} does not exist for contact {name.capitalize()}."
        return result

    def _check_contact_exist(self, name: str) -> Union[Record, str]:
        record = self.bot.book.find(name)
        if not record:
            return f"Contact {name.capitalize()} does not exist."
        else:
            return record

    def _delete_contact(self, *args) -> str:
        name = args[0]
        result = self.bot.book.delete(name)
        if result:
            return f"Contact {name.capitalize()} has been deleted."
        return f"Contact {name.capitalize()} does not exist."

    def _get_all(self) -> None:
        for record in self.bot.book.get_all_records():
            print(f"{record.name.value.capitalize()}:\t{', '.join(phone.value for phone in record.phones)}")

    @input_error_handler
    def _get_phone(self, *args) -> str:
        name = args[0]
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            return f"{name.capitalize()}: {', '.join(phone.value for phone in result.phones)}"
        return result

    @input_error_handler
    def _add_birthday(self, *args) -> str:
        name, birthday = args
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            result.add_birthday(birthday)
            return f"Birthday for {name.capitalize()} has been added."
        return result

    @input_error_handler
    def _show_birthday(self, *args) -> str:
        name = args[0]
        result = self.bot.book.find(name)
        if isinstance(result, Record):
            return f"{name.capitalize()}: {result.birthday.value}"
        return result

    @input_error_handler
    def _get_birthdays_per_week(self) -> None:
        self.bot.book.get_birthdays_per_week()

    def _exit_bot(self) -> str:
        return "Goodbye!"

    def _hello_bot(self) -> str:
        return "How can I help you?"
