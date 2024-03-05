import json
import os

from bot_constants import BOT_STATE_FILE
from contacts import AddressBook

def recall_bot_state(bot: "ConsoleBot"):
    if os.path.exists(BOT_STATE_FILE):
        with open(BOT_STATE_FILE, "r") as f:
            data = json.load(f)
            bot.book = AddressBook.from_dict(data)


def save_bot_state(bot: "ConsoleBot"):
    with open(BOT_STATE_FILE, "w") as f:
        data = bot.book.to_dict()
        json.dump(data, f, indent=4)
