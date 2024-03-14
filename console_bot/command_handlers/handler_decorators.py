from functools import wraps

from handler_exceptions import CommandException


def error_handler(func):
    """A decorator to handle input errors."""
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print(str(ex))
    return inner


def check_command_args(func):
    """A decorator to check command arguments."""
    @wraps(func)
    def inner(*args, **kwargs):
        if len(args) < 2:
            names = {"_add": "add", "_delete": "delete/remove", "_get": "get", "_get_all": "get-all", "_update": "edit"}
            raise CommandException(f"Invalid number of arguments for {names[func.__name__]} command, please try again.")
        handler, command, *args = args[0], args[1].lower(), *args[2:]
        if func.__name__ == "_add":
            if command not in ["contact", "note", "tags"]:
                raise CommandException(f"Invalid command {command}, please try again.")
        elif func.__name__ == "_delete":
            if command not in ["contact", "note"]:
                raise CommandException(f"Invalid command {command}, please try again.")
        elif func.__name__ == "_get":
            if command not in ["contact", "note"]:
                raise CommandException(f"Invalid command {command}, please try again.")
        elif func.__name__ == "_get_all":
            if command not in ["contacts", "notes", "birthdays"]:
                raise CommandException(f"Invalid command {command}, please try again.")
        elif func.__name__ == "_update":
            if command not in ["contact", "note"]:
                raise CommandException(f"Invalid command {command}, please try again.")
        else:
            raise CommandException(f"Invalid command {command}, please try again.")
        return func(handler, command, *args, **kwargs)
    return inner


def apply_decorator_to_class_methods(decorator):
    def decorate(cls):
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not attr_name.startswith("__"):
                setattr(cls, attr_name, decorator(attr))
        return cls
    return decorate