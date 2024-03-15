import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import prompt

from bot_memory import recall_bot_state, save_bot_state
from utils import _find_best_match, _parse_input
from prompt_toolkit.styles import Style

green_style = Style.from_dict({
     '': 'green',
})

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

    def bot_event_loop(self):
        """The main event loop for the bot."""
        self.commands["help"]()
        while True:
            user_input = prompt(" > Enter a command: ", style=green_style).strip()
            command, *args = _parse_input(user_input)
            result = self.commands[command](*args)
            if result:
                print(result)
                if command in ["exit", "close"]:
                    self._save_handler(self)
                    break

    def event_loop_error_handler(self, func):
        """A decorator to handle exceptions in the event loop."""
        def inner(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except (KeyError, ValueError) as ex:
                    f = ex.args[0]
                    match = _find_best_match(f, self.commands.keys())
                    if match:
                        print(f"Invalid command '{f}', did you mean '{match}'?")
                    print("Please try again.")
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    self._save_handler(self)
                    sys.exit(0)

        return inner

    def run(self, recall_state=True):
        """Run the bot."""
        if recall_state:
            self._recall_handler(self)
        event_loop = self.event_loop_error_handler(self.bot_event_loop)
        event_loop()
