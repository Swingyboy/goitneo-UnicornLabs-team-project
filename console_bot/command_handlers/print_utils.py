from typing import List, Union
from prettytable import PrettyTable, DOUBLE_BORDER

def colorize(text, color_code, bold=False):
    bold_code = "\033[1m" if bold else ""
    reset_code = "\033[0m"
    return f"{bold_code}\033[{color_code}m{text}{reset_code}"

def _pprint_notes(notes: Union[List["Note"], "Note"]):
    """Pretty print the notes"""
    table = PrettyTable()
    table.title = colorize("My Notes", 34, bold=True)  # Blue bold heading
    table.field_names = [colorize("Index", 32), colorize("Summary", 32), colorize("Text", 32), colorize("Tags", 32)]
    table.align = "l"  # Align text to the left (subheadings included)
    table.set_style(DOUBLE_BORDER)  # Change the frame style
    table.padding_width = 1  # Setting the indent between columns

    if not isinstance(notes, list):
        notes = [notes]

    for note in notes:
        tags = ', '.join([tag.value for tag in note.tags])
        table.add_row([note.index, note.summary.value, note.text.value, tags])

    print(table)


def _pprint_records(records: Union[List["Record"], "Record"]):
    """Pretty print the records"""
    table = PrettyTable()
    table.title = colorize("My Address Book", 34, bold=True)
    table.field_names = [
        colorize("Name", 32), 
        colorize("Phone", 32), 
        colorize("Birthday", 32), 
        colorize("Email", 32), 
        colorize("Address", 32)
    ]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    table.padding_width = 1

    if not isinstance(records, list):
        records = [records]

    for record in records:
        row = [record.name.value, record.phone.value]
        if record.birthday:
            row.append(record.birthday.value)
        else:
            row.append("—")  # Instead of None, added "—" for a better visual representation
        if record.email:
            row.append(record.email.value)
        else:
            row.append("—")
        if record.address:
            row.append(record.address.value)
        else:
            row.append("—")
        table.add_row(row)

    print(table)

def _print_birthdays(records: dict):
    """Print the birthdays."""
    table = PrettyTable()
    table.title = colorize("Upcoming Birthdays", 34, bold=True)
    table.field_names = [
        colorize("Day", 32), 
        colorize("Contacts", 32)
    ]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    table.padding_width = 1

    for day, contacts in records.items():
        table.add_row([day, contacts])

    print(table)


def _print_help(handler: "BaseCommandHandler"):
    """Print the help message."""
    print('''
                                 _         _             _   
                                | |       | |           | |  
   ___  ___   _ __   ___   ___  | |  ___  | |__    ___  | |_ 
  / __|/ _ \\ | '_ \\ / __| / _ \\ | | / _ \\ | '_ \\  / _ \\ | __|
 | (__| (_) || | | |\\__ \\| (_) || ||  __/ | |_) || (_) || |_ 
  \___|\\___/ |_| |_||___/ \___/ |_| \___| |_.__/  \___/  \__|
                                      ______                 
                                     |______|     
                                    
Made by UnicornLabs                                   
''')


    print("Available commands:")
    table = PrettyTable()
    table.title = colorize("Help Commands", 34, bold=True)
    table.field_names = [
        colorize("Command", 32), 
        colorize("Description", 32)
    ]
    table.align = "l"
    table.set_style(DOUBLE_BORDER)
    table.padding_width = 1

    for command, func in handler.SUPPORTED_COMMANDS.items():
        table.add_row([command, func.__doc__])

    print(table)
