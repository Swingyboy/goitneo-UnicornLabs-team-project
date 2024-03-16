import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import prompt

from bot_memory import recall_bot_state, save_bot_state
from utils import _find_best_match, _parse_input
from prompt_toolkit.styles import Style


RED_COLOR = "\033[91m"
WHITE_COLOR = "\033[97m"

our_style = Style.from_dict({
    '': 'yellow',
    'before': 'cyan',
})

message = [
    ('class:before', '> Enter a command: ')
]

class ConsoleBot:
    """A class to represent a console bot."""
    def __init__(self,
                 address_book: "AddressBook",
                 command_handler: "BaseCommandHandler",
                 note_book: "NoteBook"
                 ) -> None:
        self._save_handler = save_bot_state
        self._recall_handler = recall_bot_state
        self.address_book = address_book
        self.note_book = note_book
        self.handler = command_handler(self)
        self.commands = self.handler.SUPPORTED_COMMANDS
        self.prmt_session = PromptSession()
        self.__first_run = True

    def bot_event_loop(self):
        """The main event loop for the bot."""
        self.commands["help"](print_starting=self.__first_run)
        self.__first_run = False
        while True:
            user_input = prompt(message, style=our_style).strip().lower()
            command, *args = _parse_input(user_input)
            self.commands[command](*args)

    def event_loop_error_handler(self, func, recall_state=True):
        """A decorator to handle exceptions in the event loop."""
        def inner(*args, **kwargs):
            try:
                if recall_state:
                    self._recall_handler(self)
            except MemoryError as ex:
                print(RED_COLOR + str(ex) + WHITE_COLOR)
            while True:
                try:
                    return func(*args, **kwargs)
                except (KeyError, ValueError) as ex:
                    f = ex.args[0]
                    match = _find_best_match(f, self.commands.keys())
                    if match:
                        print(RED_COLOR + f"Invalid command '{f}', did you mean '{match}'?" + WHITE_COLOR)
                    print(RED_COLOR + f"Invalid command '{f}'. Please try again." + WHITE_COLOR)
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    self._save_handler(self)
                    sys.exit(0)
                except MemoryError as ex:
                    print(RED_COLOR + str(ex) + WHITE_COLOR)
                    sys.exit(1)
        return inner

    def run(self, recall_state=True):
        """Run the bot."""
        event_loop = self.event_loop_error_handler(self.bot_event_loop, recall_state=recall_state)
        event_loop()