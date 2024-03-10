import json
import os

from bot_constants import BOT_STATE_FILE
from contacts import AddressBook, NoteBook


def recall_bot_state(bot: "ConsoleBot"):
    if os.path.exists(BOT_STATE_FILE):
        with open(BOT_STATE_FILE, "r") as f:
            data = json.load(f)
            bot.address_book = AddressBook.from_dict(data.get("addressBook", []))
            bot.note_book = NoteBook.from_dict(data.get("noteBook", []))


def save_bot_state(bot: "ConsoleBot"):
    with open(BOT_STATE_FILE, "w") as f:
        data = {"addressBook": bot.address_book.to_dict(), "noteBook": bot.note_book.to_dict()}
        json.dump(data, f, indent=4)
