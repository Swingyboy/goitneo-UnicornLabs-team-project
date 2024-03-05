from typing import Tuple
import sys

from contacts import AddressBook
from commands_handler import DefaultCommandHandler


class ConsoleBot:
    def __init__(self, command_handler=DefaultCommandHandler) -> None:
        self.book = AddressBook()
        self.handler = command_handler(self)
        self.commands = self.handler.SUPPORTED_COMMANDS

    def bot_event_loop(self):
        while True:
            user_input = input("Enter a command: ").strip().lower()
            command, *args = self._parse_input(user_input)
            result = self.commands[command](*args)
            if result:
                print(result)
                if command in ["exit", "close"]:
                    break

    def event_loop_error_handler(self, func):
        def inner(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except KeyError:
                    print(f"Invalid command, supported commands are:")
                    for key in self.commands.keys():
                        print(f" - {key}")
                    print("Please try again.")
                except ValueError as v_ex:
                    print(f"Invalid command, supported commands are:")
                    for key in self.commands.keys():
                        print(f" - {key}")
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    sys.exit(0)
        return inner

    def run(self):
        event_loop = self.event_loop_error_handler(self.bot_event_loop)
        event_loop()

    def _parse_input(self, user_input: str) -> Tuple[str, ...]:
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args
