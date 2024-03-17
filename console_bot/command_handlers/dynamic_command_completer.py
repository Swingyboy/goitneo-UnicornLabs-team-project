"""Module for dynamic command autocompletion."""

from prompt_toolkit.completion import Completer, Completion


commands = {
    "add": ["contact", "note", "tags"],
    "edit": ["contact", "note"],
    "delete": ["contact", "note"],
    "search": {
        "contact": ["name", "phone", "birthday", "email", "address"],
        "note": ["tag"],
    },
    "get-all": ["contacts", "notes", "birthdays"],
    "exit": [],
    "close": [],
    "help": [],
    "hello": [],
}


class DynamicCommandCompleter(Completer):
    """
    Class DynamicCommandCompleter(Completer) provides dynamic
    autocompletion for commands in an interactive interface.
    """

    def get_completions(self, document, complete_event):
        """Provides autocompletion for subcommands based on the entered text."""

        text = document.text_before_cursor
        parts = text.split()

        num_parts = len(parts)
        if num_parts == 1:
            return self._get_top_level_completions(parts[0])
        if num_parts == 2:
            return self._get_subcommand_completions(parts[0], parts[1])
        if num_parts == 3:
            return self._get_subsubcommand_completions(parts[0], parts[1], parts[2])
        return []

    def _get_top_level_completions(self, prefix):
        """Provides autocompletion for subcommands based on the entered text."""
        sorted_commands = sorted(
            commands.keys(), key=lambda x: x.startswith(prefix), reverse=True
        )
        for command in sorted_commands:
            if isinstance(commands[command], list):
                description = f"[{'/'.join(commands[command])}]"
                yield Completion(command, -len(prefix), display_meta=description)
            else:
                description = f"[{'/'.join(commands[command].keys())}]"
                yield Completion(command, -len(prefix), display_meta=description)

    def _get_subcommand_completions(self, main_command, prefix):
        """Provides autocompletion for subcommands of a given main command."""
        subcommands = commands.get(main_command, [])
        if isinstance(subcommands, dict):
            subcommands = sorted(
                subcommands.keys(), key=lambda x: x.startswith(prefix), reverse=True
            )
        elif isinstance(subcommands, list):
            subcommands = sorted(
                subcommands, key=lambda x: x.startswith(prefix), reverse=True
            )
        for subcommand in subcommands:
            if isinstance(subcommand, str):
                yield Completion(subcommand, -len(prefix))
            else:
                description = f"[{'/'.join(subcommand)}]"
                yield Completion(subcommand, -len(prefix), display_meta=description)

    def _get_subsubcommand_completions(self, main_command, sub_command, prefix):
        """Provides autocompletion for subsubcommands of a given main and sub command."""
        if isinstance(commands.get(main_command, {}), list):
            return []
        subsubcommands = commands.get(main_command, {}).get(sub_command, [])
        if isinstance(subsubcommands, dict):
            subsubcommands = subsubcommands.get(prefix, [])
        elif isinstance(subsubcommands, list):
            subsubcommands = sorted(
                subsubcommands, key=lambda x: x.startswith(prefix), reverse=True
            )
        for subsubcommand in subsubcommands:
            if isinstance(subsubcommand, str):
                yield Completion(subsubcommand, -len(prefix))
            else:
                description = f"[{'/'.join(subsubcommand)}]"
                yield Completion(subsubcommand, -len(prefix), display_meta=description)


class FieldCompleter(Completer):
    """
    Class FieldCompleter(Completer) provides autocompletion
    for subcommands based on the entered text.
    """

    def __init__(self, main_command="", sub_command="", custom_command_list=None):
        super().__init__()
        self.main_command = main_command
        self.sub_command = sub_command
        self.custom_command_list = (
            custom_command_list if custom_command_list is not None else []
        )

    def get_completions(self, document, complete_event):
        """
        The method provides autocompletion
        for subcommands based on the entered text.
        """
        text = document.text_before_cursor
        parts = text.split()

        if len(parts) == 1:
            if self.main_command and self.sub_command:
                subcommands = commands.get(self.main_command, {}).get(
                    self.sub_command, []
                )
            elif self.custom_command_list:
                subcommands = self.custom_command_list
            else:
                subcommands = []
            sorted_subcommands = sorted(
                subcommands, key=lambda x: x.startswith(parts[0]), reverse=True
            )
            for subcommand in sorted_subcommands:
                yield Completion(subcommand, start_position=-len(parts[0]))
