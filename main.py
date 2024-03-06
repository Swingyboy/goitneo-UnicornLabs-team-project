from console_bot import ConsoleBot
from console_bot.command_handlers import DefaultCommandHandler


def main():
    bot = ConsoleBot(command_handler=DefaultCommandHandler)
    bot.run()


if __name__ == "__main__":
    main()
