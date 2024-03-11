from prettytable import PrettyTable


def _pprint_notes(data):
    """Pretty print the notes"""
    table = PrettyTable()
    table.field_names = ["Index", "Message", "Tags"]

    for note in data:
        tags = ', '.join([tag.value for tag in note.tags])
        table.add_row([note.index, note.text.value, tags])

    print(table)


def _pprint_records(data):
    """Pretty print the records"""
    table = PrettyTable()
    table.field_names = ["Name", "Phone", "Birthday", "Email", "Address"]

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

