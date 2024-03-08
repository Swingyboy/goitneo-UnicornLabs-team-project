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
        name, *user_data = args
        user_data = self.__parse_contact_data(*user_data)
        if self.bot.book.find(name):
            change = input(f"Contact {name.capitalize()} already exists. Do you want to change it?")
            if change.lower() in ["yes", "y"]:
                return self._change_contact(name, user_data)
            else:
                self._hello_bot()
        else:
            record = Record(name)
            record.add_phones(user_data.get("phones"))
            record.add_email(user_data.get("email"))
            record.add_address(user_data.get("address"))
            record.add_birthday(user_data.get("birthday"))
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
        name, *user_data = args
        user_data = self.__parse_contact_data(*user_data)
        result = self._check_contact_exist(name)
        if isinstance(result, Record):
            if user_data.get("phones"):
                result.update_phones(user_data.get("phones"))
            if user_data.get("email"):
                result.update_email(user_data.get("email"))
            if user_data.get("address"):
                result.update_address(user_data.get("address"))
            if user_data.get("birthday"):
                result.update_birthday(user_data.get("birthday"))
            return f"Contact {name.capitalize()} was updated."
        return result

    def _check_contact_exist(self, name: str) -> Union[Record, str]:
        record = self.bot.book.find(name)
        if not record:
            return f"Contact {name.capitalize()} does not exist."
        else:
            return record

    @input_error_handler
    def _delete_contact(self, *args) -> str:
        name = args[0]
        result = self.bot.book.delete(name)
        if result:
            return f"Contact {name.capitalize()} has been deleted."
        return f"Contact {name.capitalize()} does not exist."

    @input_error_handler
    def _get_all(self) -> None:
        for record in self.bot.book.get_all_records():
            res = f"{record.name.value.capitalize()}:\t{', '.join(phone.value for phone in record.phones)}"
            if record.email:
                res += f"\t{record.email.value}"
            if record.birthday:
                res += f"\t{record.birthday.value}"
            if record.address:
                res += f"\t{record.address.value}"
            print(res)

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

    def __parse_contact_data(self, *data) -> Dict[str, Union[str, list]]:
        phones = [d for d in data if d.isdigit()]
        args_number = len(data)
        phones_len = len(phones)
        args_number -= phones_len
        if args_number == 0:
            return {"phones": phones}
        elif args_number == 1:
            return {"phones": phones, "birthday": data[phones_len]}
        elif args_number == 2:
            return {"phones": phones, "birthday": data[phones_len], "email": data[phones_len + 1]}
        elif args_number == 3:
            return {"phones": phones, "birthday": data[phones_len], "email": data[phones_len + 1], "address": data[phones_len + 2]}
        else:
            raise ValueError("Invalid number of arguments")
