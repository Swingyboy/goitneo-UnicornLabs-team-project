import json
import os
import sys

from bot_constants import BOT_STATE_FILE
from book_items import AddressBook, NoteBook

COLOR_RED = '\033[91m'
COLOR_WHITE = '\033[97m'


def recall_bot_state(bot: "ConsoleBot"):
    """Recall the bot's state from the last session."""
    if os.path.exists(BOT_STATE_FILE):
        with open(BOT_STATE_FILE, "r") as f:
            try:
                data = json.load(f)
                bot.address_book = AddressBook.from_dict(data.get("addressBook", []))
                bot.note_book = NoteBook.from_dict(data.get("noteBook", []))
            except json.JSONDecodeError:
                bot.address_book = AddressBook()
                bot.note_book = NoteBook()
                raise MemoryError(COLOR_RED + "ERROR: Could not recall bot state. Starting with a fresh state." + COLOR_WHITE)



def save_bot_state(bot: "ConsoleBot"):
    """Save the bot's state for the next session."""
    with open(BOT_STATE_FILE, "w") as f:
        data = {"addressBook": bot.address_book.to_dict(), "noteBook": bot.note_book.to_dict()}
        try:
            json.dump(data, f, indent=4)
        except json.JSONDecodeError:
            raise MemoryError(COLOR_RED + "ERROR: Could not save bot state." + COLOR_WHITE)
