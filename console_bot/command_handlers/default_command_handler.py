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
                # return str(t_ex)
                raise t_ex

    return inner


class DefaultCommandHandler(BaseCommandHandler):
    def __init__(self, bot: "ConsoleBot") -> None:
        super().__init__(bot)
        self.bot: "ConsoleBot" = bot

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

    def _add(self, *args) -> str:
        """Add a new item to the address book or notebook."""
        if args[0] == "contact":
            return self._add_contact()
        elif args[0] == "note":
            return self._add_note(*args[1:])
        else:
            return "Invalid command, please try again."

    def _get(self, *args) -> str:
        """Get an item from the address book or notebook."""
        if args[0] == "contact":
            return self._find_contact(*args[1:])
        elif args[0] == "note":
            return self._find_note(*args[1:])
        else:
            return "Invalid command, please try again."

    def _get_all(self, *args) -> None:
        """Show all items in the address book or notebook."""
        if args[0] == "contacts":
            self._get_contacts()
        elif args[0] == "notes":
            self._get_notes()
        else:
            print("Invalid command, please try again.")

    def _update(self, *args) -> str:
        """Update an item in the address book or notebook."""
        if args[0] == "contact":
            return self._change_contact(args[1])
        elif args[0] == "note":
            return self._change_note(args[1])
        else:
            return "Invalid command, please try again."

    def _delete(self, *args) -> str:
        """Delete an item from the address book or notebook."""
        if args[0] == "contact":
            return self._delete_contact(*args[1:])
        elif args[0] == "note":
            return self._delete_note(*args[1:])
        else:
            return "Invalid command, please try again."

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
    def _add_contact(self) -> str:
        """Add a new contact to the address book."""
        name = self.bot.session.prompt("Enter name: ")
        if record := self.bot.address_book.find(name):
            change: str = self.bot.prmt_session.promt(f"Contact {name.capitalize()} already exists. Do you want to change it? ", default="no")
            if change.lower() in ["yes", "y"]:
                return self._change_contact(record.name.value)
            else:
                self._hello_bot()
        else:
            record = Record(name)
            phone = self.bot.prmt_session.prompt("Enter phone: ")
            record.add_phone(phone)
            email = self.bot.prmt_session.prompt("Enter email: ")
            if email:
                record.add_email(email)
            address = self.bot.prmt_session.prompt("Enter address: ")
            if address:
                record.add_address(address)    
            birthday = self.bot.prmt_session.prompt("Enter birthday: ")
            if birthday:
                record.add_birthday(birthday)
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
    def _change_contact(self, name) -> str:
        """Update contact data."""
        result: Union[Record, str] = self._check_contact_exist(name)
        if isinstance(result, Record):
            update_func = {"phone": result.update_phone,
                           "email": result.update_email,
                           "address": result.update_address, 
                           "birthday": result.update_birthday, 
                           "name": result.update_name
                           }
            while True:
                field, value = self.bot.session.prompt("Specify field and value to update: ").split(" ")
                if field in ["phone", "email", "address", "birthday", "name"]:
                    update_func[field](value)
                    print (f"Field {field} for contact {name.capitalize()} was updated.")
                    resp = self.bot.session.prompt("Do you want to update another field? ", default="no")
                    if resp.lower() in ["no", "n"]:
                        break
            return f"Contact {name.capitalize()} was updated."
        return result

    @input_error_handler
    def _change_note(self, *args) -> str:
        ...

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
    def _delete_note(self, *args) -> str:
        ...

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
    def _get_contacts(self) -> None:
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

    def _get_help(self) -> None:
        """Show supported commands."""
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
