from console_bot import ConsoleBot, DefaultCommandHandler


def main():
    bot = ConsoleBot(DefaultCommandHandler)
    bot.run()


if __name__ == "__main__":
    main()
