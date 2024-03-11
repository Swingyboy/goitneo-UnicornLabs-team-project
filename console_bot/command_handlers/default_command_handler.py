from typing import Optional, Tuple, Union

from base_handler import BaseCommandHandler
from console_bot.book_items import Record
from print_utils import _pprint_notes, _pprint_records, _print_birthdays, _print_help


def input_error_handler(func):
    """A decorator to handle input errors."""
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
        except TypeError as t_ex:
            if func.__name__ == "_search_note":
                return "Invalid number of arguments for search-note command, please try again. Give me field and value please."
            else:
                return str(t_ex)

    return inner


class DefaultCommandHandler(BaseCommandHandler):
    def __init__(self, bot: "ConsoleBot") -> None:
        super().__init__(bot)
        self.bot: "ConsoleBot" = bot
        self.SUPPORTED_COMMANDS.update({"add-address": self._add_address,
                                        "add-email": self._add_email,
                                        "add-note": self._add_note,
                                        "add-tags": self._add_tags_to_note,
                                        "all-notes": self._get_notes,
                                        "delete-contact": self._delete_contact,
                                        "delete-tags": self._delete_tags_from_note,
                                        "remove-contact": self._delete_contact,
                                        "search-contact": self._find_contact,
                                        "search-note": self._find_note,
                                        }
                                       )

    def __parse_find_params(self, *args) -> Tuple[str, str]:
        """Parse the sorted-by and order parameters from the input."""
        sorted_by: str = "index"
        order: str = "asc"
        if args:
            if "sorted-by" in args:
                sorted_by = args[args.index("sorted-by") + 1]
                try:
                    order = args[args.index("sorted-by") + 2]
                except IndexError:
                    pass
        return sorted_by, order

    @input_error_handler
    def _add_address(self, *args) -> str:
        """Add address to a contact."""
        name, address = args
        result: Union["Record", str] = self._check_contact_exist(name)
        if not isinstance(result, str):
            result.add_address(address)
            return f"Address for {name.capitalize()} has been added."
        return result

    @input_error_handler
    def _add_birthday(self, *args) -> str:
        """Add birthday to a contact.
        Format should be "DD.MM.YYYY".
        """
        name, birthday = args
        result: Union["Record", str] = self._check_contact_exist(name)
        if not isinstance(result, str):
            result.add_birthday(birthday)
            return f"Birthday for {name.capitalize()} has been added."
        return result

    @input_error_handler
    def _add_contact(self, *args) -> str:
        """Add a new contact to the address book."""
        name, *user_data = args
        if self.bot.address_book.find(name):
            change: str = input(f"Contact {name.capitalize()} already exists. Do you want to change it? ")
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
        """Add email to a contact."""
        name, email = args
        result: ["Record", str] = self._check_contact_exist(name)
        if not isinstance(result, str):
            result.add_email(email)
            return f"Email for {name.capitalize()} has been added."
        return result

    @input_error_handler
    def _add_note(self, *args) -> str:
        """Add a new note to the notebook."""
        self.bot.note_book.new_note(*args)
        return "Note has been added."

    def _add_tags_to_note(self, *args) -> str:
        """Add tags to a note by index."""
        note_index, *tags = args
        note_index = int(note_index) - 1  # Note count starts from 1
        return self.bot.note_book.add_tags_to_note(note_index, *tags)

    @input_error_handler
    def _change_contact(self, *args) -> str:
        """Change contact data."""
        name, *user_data = args
        result: Union["Record", str] = self._check_contact_exist(name)
        if not isinstance(result, str):
            result.update_fields_from_tuple(*user_data)
            return f"Contact {name.capitalize()} was updated."
        return result

    @input_error_handler
    def _check_contact_exist(self, name: str) -> Union[Record, str]:
        """Check if the contact exists in the address book."""
        record: Optional["Record"] = self.bot.address_book.find(name)
        if not record:
            return f"Contact {name.capitalize()} does not exist."
        else:
            return record

    @input_error_handler
    def _delete_contact(self, *args) -> str:
        """Delete a contact from the address book."""
        name = args[0]
        result: bool = self.bot.address_book.delete(name)
        if result:
            return f"Contact {name.capitalize()} has been deleted."
        return f"Contact {name.capitalize()} does not exist."

    @input_error_handler
    def _delete_tags_from_note(self, *args) -> str:
        """Delete tags from a note by index."""
        note_index, *tags = args
        note_index = int(note_index) - 1  # Note count starts from 1
        return self.bot.note_book.delete_tags_from_note(note_index, *tags)

    @input_error_handler
    def _find_contact(self, by_field: str, value: str) -> Optional[str]:
        """Find a contact by a given field and value."""
        result: Optional[str] = self.bot.address_book.search(by_field, value)
        if result:
            _pprint_records(result)
            return
        return f"No book_items found with {by_field} {value}."

    @input_error_handler
    def _find_note(self, by_field: str, value: str, *args) -> str:
        """Find a note by a given field and value."""
        sorted_by, order = self.__parse_find_params(*args)
        result = self.bot.note_book.search(by_field, value, sorted_by, order)
        if result:
            return_str = ""
            _pprint_notes(result)
            return return_str
        return f"No notes found with {by_field} {value}."

    @input_error_handler
    def _get_all(self) -> None:
        """Show all book_items in the address book."""
        records = self.bot.address_book.get_all_records()
        if not records:
            print("The address book is empty.")
        _pprint_records(records)

    @input_error_handler
    def _get_birthdays_from_date(self, *args) -> None:
        """Show birthdays for the next n days. By default, n=7."""
        try:
            number_of_days: int = int(args[0])
        except IndexError:
            number_of_days = 7
        except ValueError:
            raise ValueError("Invalid number of days.")
        result = self.bot.address_book.get_birthdays_per_week(number_of_days)
        if result:
            _print_birthdays(result)

    def _get_help(self) -> str:
        """Show supported commands."""
        # return ("Supported commands:\n"
        #         "add <name> <phone> [birthday] [email] [address] - add a new contact\n"
        #         "add-birthday <name> <birthday> - add birthday to a contact\n"
        #         "add-email <name> <email> - add email to a contact\n"
        #         "add-address <name> <address> - add address to a contact\n"
        #         "all - show all book_items\n"
        #         "change <name> [new_phone] [new_birthday] [new_email] [new_address] - change contact\n"
        #         "delete <name> - delete contact\n"
        #         "exit, close - close the program\n"
        #         "hello - display welcome message\n"
        #         "phone <name> - show phone number\n"
        #         "show-birthday <name> - show birthday\n"
        #         "birthdays - show birthdays for the next 7 days\n"
        #         "help - show this message\n"
        #         )
        _print_help(self)

    @input_error_handler
    def _get_notes(self):
        """Show all notes in the notebook."""
        _pprint_notes(self.bot.note_book.data)

    @input_error_handler
    def _get_phone(self, *args) -> str:
        """Show phone number for a contact."""
        name = args[0]
        result = self._check_contact_exist(name)
        if not isinstance(result, str):
            return f"{name.capitalize()}: {result.phone.value}"
        return result

    @input_error_handler
    def _show_birthday(self, *args) -> str:
        """Show birthday for a contact."""
        name = args[0]
        result: Optional["Record"] = self.bot.address_book.find(name)
        if result:
            return f"{name.capitalize()}: {result.birthday.value}"
        return f"The birthday date is not specified for {name.capitalize()} contact."

    def _exit_bot(self) -> str:
        """Exit the bot."""
        return "Goodbye!"

    def _hello_bot(self) -> str:
        """Greet the bot."""
        return "How can I help you?"
