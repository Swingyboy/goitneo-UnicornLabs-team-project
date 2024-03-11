import sys

from bot_memory import recall_bot_state, save_bot_state
from book_items import AddressBook, NoteBook
from utils import _find_best_match, _parse_input


class ConsoleBot:
    def __init__(self, command_handler: "BaseCommandHandler") -> None:
        self.address_book = AddressBook()
        self.note_book = NoteBook()
        self.handler = command_handler(self)
        self.commands = self.handler.SUPPORTED_COMMANDS

    def bot_event_loop(self):
        while True:
            user_input = input("Enter a command: ").strip().lower()
            command, *args = _parse_input(user_input)
            result = self.commands[command](*args)
            if result:
                print(result)
                if command in ["exit", "close"]:
                    save_bot_state(self)
                    break

    def event_loop_error_handler(self, func):
        def inner(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except (KeyError, ValueError) as ex:
                    f = ex.args[0]
                    match = _find_best_match(f, self.commands.keys())
                    if match:
                        print(f"Invalid command '{f}', did you mean '{match}'?")
                    else:
                        print(f"Invalid command, use 'help' to see supported commands.")
                    print("Please try again.")
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    save_bot_state(self)
                    sys.exit(0)

        return inner

    def run(self, recall_state=True):
        if recall_state:
            recall_bot_state(self)
        event_loop = self.event_loop_error_handler(self.bot_event_loop)
        event_loop()
