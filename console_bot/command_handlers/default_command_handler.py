import sys
from typing import Optional


from base_handler import BaseCommandHandler
from console_bot.book_items import Record, Note
from handler_exceptions import BaseHandlerException, CommandException
from handler_decorators import apply_decorator_to_class_methods, check_command_args, error_handler
from print_utils import _pprint_notes, _pprint_records, _print_birthdays, _print_help
from collections import namedtuple

from prompt_toolkit.shortcuts import prompt
from fields import PhoneValidator, EmailValidator, DateValidator
from prompt_toolkit.completion import WordCompleter


GREEN_COLOR = "\033[92m"
RED_COLOR = "\033[91m"
WHITE_COLOR = "\033[97m"


@apply_decorator_to_class_methods(error_handler)
class DefaultCommandHandler(BaseCommandHandler):
    def __init__(self, bot: "ConsoleBot") -> None:
        super().__init__(bot)
        self.bot: "ConsoleBot" = bot

        self.cmd_phone = "phone"
        self.cmd_email = "email"
        self.cmd_birthday = "birthday"
        self.cmd_address = "address"
        self.cmd_name = "name"

        self.validators = {
            self.cmd_phone : PhoneValidator(),
            self.cmd_email: EmailValidator(),
            self.cmd_birthday: DateValidator(),
        }

    @check_command_args
    def _add(self, command, *args) -> None:
        """Add a new contact or note. Format 'add [contact/note]'."""
        if command == "contact":
            name = " ".join(args)
            self._add_contact(name)
        elif command == "note":
            summary = " ".join(args)
            self._add_note(summary)
        elif command == "tags":
            self._add_tags_to_note(*args)
        
    def _add_contact(self, name: str = None) -> None:
        """Add a new contact to the address book."""
        if not name:
            name = self.bot.prmt_session.prompt("Enter name: ")
        if record := self.bot.address_book.find(name):
            change: str = self.bot.prmt_session.prompt(f"Contact {name} already exists. Do you want to change it? ", default="no")
            if change.lower() in ["yes", "y"]:
                try:
                    self._change_contact(record.name.value)
                except AttributeError:
                    raise BaseHandlerException(RED_COLOR + f"Contact name is incorrect: {record}." + WHITE_COLOR)
            else:
                self._hello_bot()
        else:
            record = Record(name)
            phone = prompt("Enter phone: ", validator=self.validators[self.cmd_phone])
            record.add_phone(phone)
            email = prompt("Enter email: ", validator=self.validators[self.cmd_email])
            if email:
                record.add_email(email)
            address = self.bot.prmt_session.prompt("Enter address: ")
            if address:
                record.add_address(address)    
            birthday = prompt("Enter birthday[DD.MM.YYYY]: ", validator=self.validators[self.cmd_birthday], validate_while_typing=False)
            if birthday:
                record.add_birthday(birthday)
            self.bot.address_book.add_record(record)
            print(GREEN_COLOR + f"Contact {name} has been added." + WHITE_COLOR)

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
        print(GREEN_COLOR + "Note has been added." + WHITE_COLOR)

    def _add_tags_to_note(self, *tags) -> None:
        """Add tags to a note by index."""
        note_index = self.bot.prmt_session.prompt("Enter note index to witch you want to add tags: ")
        note_index = int(note_index) - 1  # Note count starts from 1
        tags = list(tags)
        if self.bot.note_book.add_tags_to_note(note_index, tags):
            print(GREEN_COLOR + f"Tags {tags} have been added to note {note_index + 1}." + WHITE_COLOR)
            return
        else:
            print(RED_COLOR + f"Adding tags to note {note_index + 1} was failed." + WHITE_COLOR)
            
    def _change_contact(self, name: Optional[str] = None) -> None:
        """Update contact data."""
        if not name:
            # список всех контактов
            contact_names = self.get_all_contact_names()
            if not contact_names:
                print("The book is empty.")
                return
            # список с возможностью выбора
            print("Select contact to edit:")
            for index, name in enumerate(contact_names):
                print(f"{index + 1}. {name}")
            # пока не введется корректный индекс
            names_completer = WordCompleter(contact_names)
            while True:
                # индекс выбранного контакта
                inputed = prompt("Enter contact number or name: ", completer=names_completer)
                index=0
                if inputed.isdigit() and 1 <= int(inputed) <= len(contact_names):
                    index = int(inputed)
                    break
                elif inputed in contact_names:
                    index=contact_names.index(inputed)+1
                    break
                else:
                    print("Invalid input. Please enter a valid contact number.")
            # имя выбранного контакта
            name = contact_names[int(index) - 1]
            print(f"Selected contact: {name}")
        # запись выбранного контакта
        selected_contact = self.bot.address_book.find(name)
        if selected_contact:
            update_func = {
                self.cmd_phone: selected_contact.update_phone,
                self.cmd_email: selected_contact.update_email,
                self.cmd_address: selected_contact.update_address,
                self.cmd_birthday: selected_contact.update_birthday,
                self.cmd_name: selected_contact.update_name
            }
            while True:
                # список полей контакта для редактирования
                print("Select field to edit:")
                for index, field in enumerate(selected_contact.to_dict().keys()):
                    print(f"{index + 1}. {field}")
                # поле для редактирования
                field_index = self.bot.prmt_session.prompt("Enter field number: ")
                if field_index.isdigit():
                    field_index = int(field_index)
                    # является ли ввод числом и корректным индексом
                    if 1 <= field_index <= len(selected_contact.to_dict().keys()):
                        field_name = list(selected_contact.to_dict().keys())[field_index - 1]
                        # новое значение для выбранного поля
                        old_value = selected_contact.to_dict().get(field_name)
                        new_value = prompt(f"Enter new {field_name}: ", default=old_value, validator=self.validators.get(field_name))
                        update_func[field_name](new_value)
                        print(GREEN_COLOR + f"Field '{field_name}' for contact '{name}' was updated from '{old_value}' to '{new_value}'" + WHITE_COLOR)
                        # обновить другие поля
                        resp = self.bot.prmt_session.prompt("Do you want to update another field? ", default="no")
                        if resp.lower() in ["no", "n"]:
                            break
                        else:
                            continue
                else:
                    print(RED_COLOR + "Invalid input. Please enter a valid field number." + WHITE_COLOR)
                    continue
                print(GREEN_COLOR + f"Contact {name} was updated." + WHITE_COLOR)
        else:
            print(RED_COLOR + f"Contact {name} does not exist." + WHITE_COLOR)

    def get_all_contact_names(self):
        contacts = self.bot.address_book.get_all_records()
        if not contacts:
            return []

        return [contact.name.value for contact in contacts]

    def _change_note(self, index:int = None) -> None:
        """Change the text of a note."""
        if not index:
            # список всех notes из noteBook
            notes = self.bot.note_book.get_all_notes()
            if not notes:
                return "The book is empty."     
            # список для редактирования
            name_notes = [note.summary.value for note in notes]
            # возможность выбора
            print("Select notes to edit:")
            for index, name in enumerate(name_notes):
                print(f"{index + 1}. {name}")
            while True:
                index = self.bot.prmt_session.prompt("Enter notes number: ")
                # является ли ввод числом и корректным индексом
                if index.isdigit() and 1 <= int(index) <= len(name_notes):
                    index = int(index)
                    break
                else:
                    print(RED_COLOR + "Invalid input. Please enter a valid note number." + WHITE_COLOR)
            name = name_notes[int(index) - 1]
            
            selected_note = self.bot.note_book.find(name)
        else:
           selected_note = self._check_note_exist(index)
           name = selected_note.summary.value

        print(f"Selected note: {name}")
        # список полей для редактирования
        print("Select field to edit:")
        for index, field in enumerate(selected_note.to_dict().keys()):
            print(f"{index + 1}. {field}")
        # функции для обновления каждого поля
        update_func = {
            "summary": selected_note.update_summary,
            "text": selected_note.update_text,
            "tags": selected_note.update_tags
            }
        while True:
            # выбранное поле для редактирования
            field_index = self.bot.prmt_session.prompt("Enter field number: ")
            if field_index.isdigit():
                field_index = int(field_index)
                if 1 <= field_index <= len(selected_note.to_dict().keys()):
                    field_name = list(selected_note.to_dict().keys())[field_index - 1]
                    # новое значение для выбранного поля
                    old_value = selected_note.to_dict().get(field_name)
                    if isinstance(old_value, list):
                        old_value = ", ".join(old_value)
                    new_value = self.bot.prmt_session.prompt(f"Enter new {field_name}: ", default=old_value)
                    # поле записи
                    update_func[field_name](new_value)
                    print(GREEN_COLOR + f"Field {field_name} for note '{name}' was updated." + WHITE_COLOR)
                    # желание обновить другие поля
                    resp = self.bot.prmt_session.prompt("Do you want to update another field? ", default="no")
                    if resp.lower() in ["no", "n"]:
                        break
            else:
                print(RED_COLOR + "Invalid input. Please enter a valid field number." + WHITE_COLOR)

        print(GREEN_COLOR + f"Note '{name}' was updated." + WHITE_COLOR)

    def _check_contact_exist(self, name: str) -> Optional[Record]:
        """Check if the contact exists in the address book."""
        record: Optional["Record"] = self.bot.address_book.find(name)
        if not record:
            print(RED_COLOR + f"Contact {name} does not exist." + WHITE_COLOR)
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
        """Delete/remove an item from the address book or notebook. Format 'remove/delete [contact/note]"""
        if command == "contact":
            name = " ".join(args)
            self._delete_contact(name)
        elif command == "note":
            index = " ".join(args)
            self._delete_note(index)
        
    def _delete_contact(self, name: str = None) -> None:
        """Delete a contact from the address book."""
        contact_names = self.get_all_contact_names()
        if not contact_names:
            print("The book is empty.")
            return
        names_completer = WordCompleter(contact_names)

        if not name:
            name = prompt("Enter the name of the contact you want to delete: ", completer=names_completer)
        result: bool = self.bot.address_book.delete_record(name)
        if result:
            print(GREEN_COLOR + f"Contact {name} has been deleted." + WHITE_COLOR)
        else:
            print(RED_COLOR + f"Contact {name} does not exist." + WHITE_COLOR)

    def _delete_note(self, index: int = None) -> None:
        """Delete a note from the notebook."""
        if not index:
            index = self.bot.prmt_session.prompt("Enter the index of the note you want to delete: ")
        try:
            index = int(index)
        except ValueError:
            raise BaseCommandHandler(f"Invalid index {index}. Index should be a number, current index is {index}.")
        if self.bot.note_book.delete_note(index):
            print(GREEN_COLOR + f"Note {index} has been deleted." + WHITE_COLOR)
            return
        print(RED_COLOR + f"Note {index} does not exist." + WHITE_COLOR)

    def _delete_tags_from_note(self, *args) -> None:
        """Delete tags from a note by index."""
        try:
            note_index, *tags = args
        except ValueError:
            raise CommandException("Invalid number of arguments for delete-tags command, please try again.")
        note_index = int(note_index) - 1  # Note count starts from 1
        if self.bot.note_book.delete_tags_from_note(note_index, *tags):
            print(GREEN_COLOR + f"Tags {tags} have been deleted from note {note_index + 1}." + WHITE_COLOR)
        else:
            print(GREEN_COLOR + f"Deleting tags from note {note_index + 1} was failed." + WHITE_COLOR)
    
    def _exit_bot(self) -> None:
        """Exit the bot and save your data."""
        print("Saving the state...")
        self.bot._save_handler(self.bot)
        print("Done! Goodbye!")
        sys.exit(0)

    def _find_contact(self) -> None:
        """Find a contact by a given field and value."""
        by_field = self.bot.prmt_session.prompt("Enter field to search by: ")
        value = self.bot.prmt_session.prompt(f"Enter expected {by_field} value: ")
        if result := self.bot.address_book.search(by_field.lower(), value):
            _pprint_records(result)
            return
        print(RED_COLOR + f"No contacts found with {by_field} {value}." + WHITE_COLOR)

    def _find_note(self) -> None:
        """Find a note by a given field and value."""
        by_field = self.bot.prmt_session.prompt("Enter field to search by: ")
        value = self.bot.prmt_session.prompt(f"Enter expected {by_field} value: ")
        order = self.bot.prmt_session.prompt("Enter order (asc/desc): ", default="asc")
        if result := self.bot.note_book.search(by_field, value, by_field, order):
            _pprint_notes(result)
            return
        print(RED_COLOR + f"No notes found with {by_field} {value}." + WHITE_COLOR)


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
            print(RED_COLOR + "Invalid command, please try again." + WHITE_COLOR)
    
    def _get_contacts(self) -> None:
        """Show all book_items in the address book."""
        records = self.bot.address_book.get_all_records()
        if not records:
            print(RED_COLOR + "The address book is empty." + WHITE_COLOR)
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
            print(RED_COLOR + "The notebook is empty." + WHITE_COLOR)
        _pprint_notes(notes)

    def _get_help(self, print_starting: bool = False, *args) -> None:
        """Show supported commands."""
        _print_help(self, print_title=print_starting)
        
    @check_command_args  
    def _update(self, command, *args) -> None:
        """Update an item in the address book or notebook. Format 'edit [contact/note]"""
        if command == "contact":
            self._change_contact(*args)
        elif command == "note":
            self._change_note(*args)

    def _hello_bot(self) -> None:
        """Greet the bot."""
        print("How can I help you? Use 'help' command to see available commands.")
