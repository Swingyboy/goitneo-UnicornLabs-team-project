from typing import Optional, Tuple, Union

from base_handler import BaseCommandHandler
from console_bot.book_items import Record, Note
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

    def _add(self, *args) -> str:
        """Add a new item to the address book or notebook."""
        command = args[0].lower()
        if command == "contact":
            return self._add_contact(*args[1:])
        elif command == "note":
            return self._add_note(*args[1:])
        else:
            return "Invalid command, please try again."
        
    @input_error_handler
    def _add_contact(self, name: str = None) -> str:
        """Add a new contact to the address book."""
        if not name:
            name = self.bot.prmt_session.prompt("Enter name: ")
        if record := self.bot.address_book.find(name):
            change: str = self.bot.prmt_session.prompt(f"Contact {name.capitalize()} already exists. Do you want to change it? ", default="no")
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
    def _add_note(self, summary: str = None) -> str:
        """Add a new note to the notebook."""
        if not summary:
            summary = self.bot.prmt_session.prompt("Enter the note summary: ")
        text = self.bot.prmt_session.prompt("Enter the note text: ")
        tags = self.bot.prmt_session.prompt("Enter tags separated by commas: ")
        if tags:
            tags = tags.split(",")
            tags = [tag.strip() for tag in tags]
        else:
            tags = None
        self.bot.note_book.add_note(summary=summary, text=text, tags=tags)
        return "Note has been added."

    def _add_tags_to_note(self, *args) -> str:
        """Add tags to a note by index."""
        note_index, *tags = args
        note_index = int(note_index) - 1  # Note count starts from 1
        return self.bot.note_book.add_tags_to_note(note_index, *tags)
    
    @input_error_handler
    def _change_contact(self, name: Optional[str] = None) -> str:
        """Update contact data."""
        if not name:
            name = self.bot.prmt_session.prompt("Enter the name of the contact you want to edit: ")
        if result := self._check_contact_exist(name):
            update_func = {"phone": result.update_phone,
                           "email": result.update_email,
                           "address": result.update_address, 
                           "birthday": result.update_birthday, 
                           "name": result.update_name
                           }
            while True:
                field = self.bot.prmt_session.prompt("Specify field you want to update: ")
                value = self.bot.prmt_session.prompt(f"Enter new {field}: ")
                if field in ["phone", "email", "address", "birthday", "name"]:
                    update_func[field](value)
                    print (f"Field {field} for contact {name.capitalize()} was updated.")
                    resp = self.bot.prmt_session.prompt("Do you want to update another field? ", default="no")
                    if resp.lower() in ["no", "n"]:
                        break
            return f"Contact {name.capitalize()} was updated."
        return result

    @input_error_handler
    def _change_note(self, index:int = None) -> str:
        """Change the text of a note."""
        if not index:
            index = self.bot.prmt_session.prompt("Enter the index of the note you want to edit: ")
        if result := self._check_note_exist(index):
            update_func = {"summary": result.add_summary,
                           "text": result.add_text,
                           "tags": result.add_tags
                           }
            while True:
                field = self.bot.prmt_session.prompt("Specify field you want to update: ")
                if field in ["summary", "text"]:
                    value = self.bot.prmt_session.prompt(f"Enter new {field}: ")
                elif field == "tags":
                    value = self.bot.prmt_session.prompt("Enter new tags separated by commas: ")
                    if value:
                        value = value.split(",")
                else:
                    raise ValueError("Invalid field.")
                update_func[field](value)
                print (f"Field {field} for note {index} was updated.")
                resp = self.bot.prmt_session.prompt("Do you want to update another field? ", default="no")
                if resp.lower() in ["no", "n"]:
                        break
            return f"Note {index} was updated."
        return result

    @input_error_handler
    def _check_contact_exist(self, name: str) -> Optional[Record]:
        """Check if the contact exists in the address book."""
        record: Optional["Record"] = self.bot.address_book.find(name)
        if not record:
            print(f"Contact {name.capitalize()} does not exist.")
        else:
            return record
        
    @input_error_handler
    def _check_note_exist(self, index: int) -> Optional[Note]:
        """Check if the note exists in the notebook."""
        index = int(index)
        try:
            note = self.bot.note_book.get_all_notes()[index - 1]
            return note
        except IndexError:
            return f"Note with index {index} does not exist."
        
    def _delete(self, *args) -> str:
        """Delete an item from the address book or notebook."""
        command = args[0].lower()
        if command == "contact":
            return self._delete_contact(*args[1:])
        elif command == "note":
            return self._delete_note(*args[1:])
        else:
            return "Invalid command, please try again."
        
    @input_error_handler
    def _delete_contact(self, name: str = None) -> str:
        """Delete a contact from the address book."""
        if not name:
            name = self.bot.prmt_session.prompt("Enter the name of the contact you want to delete: ")
        result: bool = self.bot.address_book.delete_record(name)
        if result:
            return f"Contact {name.capitalize()} has been deleted."
        return f"Contact {name.capitalize()} does not exist."

    @input_error_handler
    def _delete_note(self, index: int = None) -> str:
        """Delete a note from the notebook."""
        if not index:
            index = self.bot.prmt_session.prompt("Enter the index of the note you want to delete: ")
        index = int(index)
        if self.bot.note_book.delete_note(index):
            return f"Note {index} has been deleted."
        return f"Note {index} does not exist."

    @input_error_handler
    def _delete_tags_from_note(self, *args) -> str:
        """Delete tags from a note by index."""
        note_index, *tags = args
        note_index = int(note_index) - 1  # Note count starts from 1
        return self.bot.note_book.delete_tags_from_note(note_index, *tags)
    
    def _exit_bot(self) -> str:
        """Exit the bot."""
        return "Goodbye!"
    
    @input_error_handler
    def _find_contact(self) -> Optional[str]:
        """Find a contact by a given field and value."""
        by_field = self.bot.prmt_session.prompt("Enter field to search by: ")
        value = self.bot.prmt_session.prompt(f"Enter expected {by_field} value: ")
        result: Optional[str] = self.bot.address_book.search(by_field.lower(), value)
        if result:
            _pprint_records(result)
            return
        return f"No contacts found with {by_field} {value}."

    @input_error_handler
    def _find_note(self) -> str:
        """Find a note by a given field and value."""
        by_field = self.bot.prmt_session.prompt("Enter field to search by: ")
        value = self.bot.prmt_session.prompt(f"Enter expected {by_field} value: ")
        order = self.bot.prmt_session.prompt("Enter order (asc/desc): ", default="asc")
        result = self.bot.note_book.search(by_field, value, by_field, order)
        if result:
            return_str = ""
            _pprint_notes(result)
            return return_str
        return f"No notes found with {by_field} {value}."

    def _get(self, *args) -> str:
        """Get an item from the address book or notebook."""
        if args[0].lower() == "contact":
            return self._find_contact()
        elif args[0].lower() == "note":
            return self._find_note()
        else:
            return "Invalid command, please try again."

    def _get_all(self, *args) -> None:
        """Show all items in the address book or notebook."""
        command = args[0]
        if command == "contacts":
            self._get_contacts()
        elif command == "notes":
            self._get_notes()
        elif command == "birthdays":
            self._get_birthdays_from_date(*args[1:])
        else:
            print("Invalid command, please try again.")
    
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

    @input_error_handler
    def _get_notes(self) -> None:
        """Show all notes in the notebook."""
        notes = self.bot.note_book.get_all_notes()
        if not notes:
            print("The notebook is empty.")
        _pprint_notes(notes)

    def _get_help(self) -> None:
        """Show supported commands."""
        _print_help(self)

    def _update(self, *args) -> str:
        """Update an item in the address book or notebook."""
        command = args[0].lower()
        if command == "contact":
            return self._change_contact(*args[1:])
        elif command == "note":
            return self._change_note(*args[1:])
        else:
            return "Invalid command, please try again."

    def _hello_bot(self) -> str:
        """Greet the bot."""
        return "How can I help you?"
