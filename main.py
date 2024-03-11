from console_bot import ConsoleBot
from console_bot.command_handlers import DefaultCommandHandler
from console_bot.book_items import AddressBook, NoteBook


def main():
    address_book = AddressBook()
    note_book = NoteBook()
    bot = ConsoleBot(command_handler=DefaultCommandHandler,
                     address_book=address_book,
                     note_book=note_book
                     )
    bot.run()


if __name__ == "__main__":
    main()
