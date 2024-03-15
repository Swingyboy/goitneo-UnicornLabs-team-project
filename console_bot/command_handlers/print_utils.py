from typing import List, Union
from prettytable import PrettyTable


def _pprint_notes(notes: Union[List["Note"], "Note"]):
    """Pretty print the notes"""
    table = PrettyTable()
    table.field_names = ["Index", "Summary", "Text", "Tags"]

    if not isinstance(notes, list):
        notes = [notes]

    for note in notes:
        tags = ', '.join([tag.value for tag in note.tags])
        table.add_row([note.index, note.summary.value, note.text.value, tags])

    print(table)


def _pprint_records(records: Union[List["Record"], "Record"]):
    """Pretty print the records"""
    table = PrettyTable()
    table.field_names = ["Name", "Phone", "Birthday", "Email", "Address"]

    if not isinstance(records, list):
        records = [records]

    for record in records:
        name = " ".join(r.strip().capitalize() for r in record.name.value.split())
        row = [name, record.phone.value]
        if record.birthday:
            row.append(record.birthday.value)
        else:
            row.append(None)
        if record.email:
            row.append(record.email.value)
        else:
            row.append(None)
        if record.address:
            row.append(record.address.value)
        else:
            row.append(None)
        table.add_row(row)

    print(table)


def _print_birthdays(records: dict):
    """Print the birthdays."""
    table = PrettyTable()
    table.field_names = ["Day", "Contacts"]
    for day, contacts in records.items():
        table.add_row([day, contacts])

    print(table)


def _print_help(handler: "BaseCommandHandler"):
    """Print the help message."""
    print("This is contact book app.")
    print("Available commands:")
    table = PrettyTable()
    table.field_names = ["Command", "Description"]
    for command, func in handler.SUPPORTED_COMMANDS.items():
        table.add_row([command, func.__doc__])

    print(table)
