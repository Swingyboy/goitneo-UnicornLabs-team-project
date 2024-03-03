from typing import Tuple
import sys


CONTACTS = {}


def input_error_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            if func.__name__ == "_add_contact":
                return "Invalid number of arguments for add command, please try again. Give me name and phone please."
            elif func.__name__ == "_change_contact":
                return ("Invalid number of arguments for change command, please try again."
                        " Give me name and phone please.")
            elif func.__name__ == "_get_phone":
                return "Invalid number of arguments for phone command, please try again. Give me name please."
    return inner


def event_loop_error_handler(func):
    def inner(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except KeyError:
                print(f"Invalid command, supported commands are:")
                for key in SUPPORTED_COMMANDS.keys():
                    print(f" - {key}")
                print("Please try again.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                sys.exit(0)
    return inner


def _parse_input(user_input: str) -> Tuple[str, ...]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error_handler
def _add_contact(*args) -> str:
    name, phone = args
    if name in CONTACTS:
        change = input(f"Contact {name.capitalize()} already exists. Do you want to change it?")
        if change.lower() in ["yes", "y"]:
            return _change_contact(name, phone)
        else:
            _hello_bot()
    else:
        CONTACTS[name] = phone
        return f"Contact {name.capitalize()} has been added."


@input_error_handler
def _change_contact(*args) -> str:
    name, phone = args
    if name not in CONTACTS:
        return f"Contact {name.capitalize()} does not exist."
    else:
        CONTACTS[name] = phone
        return f"Contact {name.capitalize()} has been updated."


def _get_all() -> None:
    for name, phone in CONTACTS.items():
        print(f"{name.capitalize()}:\t {phone}")


def _get_phone(*args) -> str:
    name = args[0]
    if name not in CONTACTS:
        return f"Contact {name.capitalize()} does not exist."
    else:
        return f"{name.capitalize()}: {CONTACTS[name]}"


def _exit_bot() -> str:
    return "Goodbye!"


def _hello_bot() -> str:
    return "How can I help you?"


SUPPORTED_COMMANDS = {"exit": _exit_bot,
                      "close": _exit_bot,
                      "hello": _hello_bot,
                      "add": _add_contact,
                      "change": _change_contact,
                      "phone": _get_phone,
                      "all": _get_all
                      }


@event_loop_error_handler
def bot_event_loop():
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = _parse_input(user_input)
        result = SUPPORTED_COMMANDS[command](*args)
        if result:
            print(result)


def bot_main():
    print("Welcome to the assistant bot!")
    bot_event_loop()


if __name__ == "__main__":
    bot_main()
