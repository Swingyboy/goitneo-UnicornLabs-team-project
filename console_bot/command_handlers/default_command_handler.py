import sys
from typing import Optional


from base_handler import BaseCommandHandler
from console_bot.book_items import Record, Note
from handler_exceptions import BaseHandlerException, CommandException
from handler_decorators import apply_decorator_to_class_methods, check_command_args, error_handler
from print_utils import _pprint_notes, _pprint_records, _print_birthdays, _print_help

from prompt_toolkit.shortcuts import prompt
from fields import PhoneValidator, EmailValidator, DateValidator


@apply_decorator_to_class_methods(error_handler)
class DefaultCommandHandler(BaseCommandHandler):
    def __init__(self, bot: "ConsoleBot") -> None:
        super().__init__(bot)
        self.bot: "ConsoleBot" = bot

    @check_command_args
    def _add(self, command, *args) -> None:
        """Add a new contact, note or tag. Format 'add [contact/note/tags]'."""
        if command == "contact":
            self._add_contact(*args)
        elif command == "note":
            self._add_note(*args)
        elif command == "tags":
            self._add_tags_to_note(*args[1:])
        
    def _add_contact(self, name: str = None) -> None:
        """Add a new contact to the address book."""
        if not name:
            name = self.bot.prmt_session.prompt("Enter name: ")
        if record := self.bot.address_book.find(name):
            change: str = self.bot.prmt_session.prompt(f"Contact {name.capitalize()} already exists. Do you want to change it? ", default="no")
            if change.lower() in ["yes", "y"]:
                try:
                    self._change_contact(record.name.value)
                except AttributeError:
                    raise BaseHandlerException(f"Contact name is incorrect: {record}.")
            else:
                self._hello_bot()
        else:
            record = Record(name)
            phone = prompt("Enter phone: ", validator=PhoneValidator())
            record.add_phone(phone)
            email = prompt("Enter email: ", validator=EmailValidator())
            if email:
                record.add_email(email)
            address = self.bot.prmt_session.prompt("Enter address: ")
            if address:
                record.add_address(address)    
            birthday = prompt("Enter birthday[DD.MM.YYYY]: ", validator= DateValidator(), validate_while_typing=False)
            if birthday:
                record.add_birthday(birthday)
            self.bot.address_book.add_record(record)
            print(f"Contact {name.capitalize()} has been added.")

    def _add_note(self, summary: str = None) -> None:
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
        print("Note has been added.")

    def _add_tags_to_note(self, *tags) -> None:
        """Add tags to a note by index."""
        note_index = self.bot.prmt_session.prompt("Enter the index of the note: ")
        if not tags:
            tags = self.bot.prmt_session.prompt("Enter tags separated by commas: ")
            if tags:
                tags = tags.split(",")
                tags = [tag.strip() for tag in tags]
        if note := self._check_note_exist(note_index):
            note_index = int(note_index) - 1  # Note count starts from 1
            if self.bot.note_book.add_tags_to_note(note_index, tags):
                print(f"Tags {tags} have been added to note {note_index + 1}.")
            else:
                print(f"Adding tags to note {note_index + 1} was failed.")
        else:
            print(f"Note with index {note_index} does not exist.")
    
    def _change_contact(self, name: Optional[str] = None) -> None:
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
            print(f"Contact {name.capitalize()} was updated.")
            return
        print(f"Contact {name.capitalize()} does not exist.")

    def _change_note(self, index:int = None) -> None:
        """Change the text of a note."""
        if not index:
            index = self.bot.prmt_session.prompt("Enter the index of the note you want to edit: ")
        if result := self._check_note_exist(index):
            update_func = {"summary": result.update_summary,
                           "text": result.update_text,
                           "tags": result.update_tags
                           }
            while True:
                field = self.bot.prmt_session.prompt("Specify field you want to update: ")
                if field in ["summary", "text"]:
                    value = self.bot.prmt_session.prompt(f"Enter new {field}: ")
                elif field == "tags":
                    value = self.bot.prmt_session.prompt("Enter new tags separated by commas: ")
                    if value:
                        value = value.split(",")
                        value = [tag.strip() for tag in value]
                else:
                    raise BaseHandlerException(f"Invalid field {value}.")
                update_func[field](value)
                print (f"Field {field} for note {index} was updated.")
                resp = self.bot.prmt_session.prompt("Do you want to update another field? ", default="no")
                if resp.lower() in ["no", "n"]:
                        break
            print(f"Note {index} was updated.")
        print(f"Note with index {index} does not exist.")

    def _check_contact_exist(self, name: str) -> Optional[Record]:
        """Check if the contact exists in the address book."""
        record: Optional["Record"] = self.bot.address_book.find(name)
        if not record:
            print(f"Contact {name.capitalize()} does not exist.")
        else:
            return record
        
    def _check_note_exist(self, index: int) -> Optional[Note]:
        """Check if the note exists in the notebook."""
        index = int(index)
        try:
            note = self.bot.note_book.get_all_notes()[index - 1]
            return note
        except IndexError:
            print(f"Note with index {index} does not exist.")
            return None
        
    @check_command_args    
    def _delete(self, command, *args) -> None:
        """Delete an item from the address book or notebook."""
        if command == "contact":
            self._delete_contact(*args)
        elif command == "note":
            self._delete_note(*args)
        
    def _delete_contact(self, name: str = None) -> None:
        """Delete a contact from the address book."""
        if not name:
            name = self.bot.prmt_session.prompt("Enter the name of the contact you want to delete: ")
        result: bool = self.bot.address_book.delete_record(name)
        if result:
            print(f"Contact {name.capitalize()} has been deleted.")
        print(f"Contact {name.capitalize()} does not exist.")

    def _delete_note(self, index: int = None) -> None:
        """Delete a note from the notebook."""
        if not index:
            index = self.bot.prmt_session.prompt("Enter the index of the note you want to delete: ")
        try:
            index = int(index)
        except ValueError:
            raise BaseCommandHandler(f"Invalid index {index}. Index should be a number")
        if self.bot.note_book.delete_note(index):
            print(f"Note {index} has been deleted.")
        print(f"Note {index} does not exist.")

    def _delete_tags_from_note(self, *args) -> None:
        """Delete tags from a note by index."""
        try:
            note_index, *tags = args
        except ValueError:
            raise CommandException("Invalid number of arguments for delete-tags command, please try again.")
        note_index = int(note_index) - 1  # Note count starts from 1
        if self.bot.note_book.delete_tags_from_note(note_index, *tags):
            print(f"Tags {tags} have been deleted from note {note_index + 1}.")
        else:
            print(f"Deleting tags from note {note_index + 1} was failed.")
    
    def _exit_bot(self) -> None:
        """Exit the bot."""
        print("Goodbye!")
        sys.exit(0)

    def _find_contact(self) -> None:
        """Find a contact by a given field and value."""
        by_field = self.bot.prmt_session.prompt("Enter field to search by: ")
        value = self.bot.prmt_session.prompt(f"Enter expected {by_field} value: ")
        if result := self.bot.address_book.search(by_field.lower(), value):
            _pprint_records(result)
            return
        print(f"No contacts found with {by_field} {value}.")

    def _find_note(self) -> None:
        """Find a note by a given field and value."""
        by_field = self.bot.prmt_session.prompt("Enter field to search by: ")
        value = self.bot.prmt_session.prompt(f"Enter expected {by_field} value: ")
        order = self.bot.prmt_session.prompt("Enter order (asc/desc): ", default="asc")
        if result := self.bot.note_book.search(by_field, value, by_field, order):
            _pprint_notes(result)
        print(f"No notes found with {by_field} {value}.")


    @check_command_args  
    def _get(self, command, *args) -> None:
        """Get an item from the address book or notebook."""
        if command == "contact":
            self._find_contact()
        elif command == "note":
            self._find_note()

    @check_command_args  
    def _get_all(self, command, *args) -> None:
        """Show all items in the address book or notebook."""
        if command == "contacts":
            self._get_contacts()
        elif command == "notes":
            self._get_notes()
        elif command == "birthdays":
            self._get_birthdays_from_date(*args)
        else:
            print("Invalid command, please try again.")
    
    def _get_contacts(self) -> None:
        """Show all book_items in the address book."""
        records = self.bot.address_book.get_all_records()
        if not records:
            print("The address book is empty.")
        _pprint_records(records)

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

    def _get_notes(self) -> None:
        """Show all notes in the notebook."""
        apply_sort = self.bot.prmt_session.prompt("Do you want to sort the notes? ", default="no")
        if apply_sort.lower() in ["yes", "y"]:
            sort_by = self.bot.prmt_session.prompt("Enter sort attribute (index/text/tag): ")
            order = self.bot.prmt_session.prompt("Enter order (asc/desc): ", default="asc")
            notes = self.bot.note_book.get_all_notes(sort_by, order)
        else:
            notes = self.bot.note_book.get_all_notes()
        if not notes:
            print("The notebook is empty.")
        _pprint_notes(notes)

    def _get_help(self) -> None:
        """Show supported commands."""
        _print_help(self)

    @check_command_args  
    def _update(self, command, *args) -> None:
        """Update an item in the address book or notebook."""
        if command == "contact":
            self._change_contact(*args)
        elif command == "note":
            self._change_note(*args)

    def _hello_bot(self) -> None:
        """Greet the bot."""
        print("How can I help you?")
