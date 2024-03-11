from typing import List, Union
from prettytable import PrettyTable


def _pprint_notes(notes: Union[List["Note"], "Note"]):
    """Pretty print the notes"""
    table = PrettyTable()
    table.field_names = ["Index", "Message", "Tags"]

    if not isinstance(notes, list):
        notes = [notes]

    for note in notes:
        tags = ', '.join([tag.value for tag in note.tags])
        table.add_row([note.index, note.text.value, tags])

    print(table)


def _pprint_records(records: Union[List["Record"], "Record"]):
    """Pretty print the records"""
    table = PrettyTable()
    table.field_names = ["Name", "Phone", "Birthday", "Email", "Address"]

    if not isinstance(records, list):
        data = [records]

    for record in data:
        row = [record.name.value, record.phone.value]
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

