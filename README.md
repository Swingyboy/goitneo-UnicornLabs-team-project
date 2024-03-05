# Console Assistant Bot

Welcome to the Assistant Bot project! This bot helps users manage their contacts by allowing them to add, change, or retrieve phone numbers. It provides a simple command-line interface for interacting with the bot.

## Features

- Add new contacts with their phone numbers
- Change existing contact phone numbers
- Remove phone numbers from existing contacts
- Remove existing contacts
- Retrieve phone numbers for specific contacts
- Add birthday to the contacts
- View upcoming birthdays
- View all contacts and their phone numbers
- Greet users and provide assistance

## Getting Started

To use the Assistant Bot, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Ensure you have Python installed on your system. This project is compatible with Python 3.10
4. Run the bot:
   ```python console_bot.py```
   
5. Follow the on-screen instructions to interact with the bot.
 
## Usage

Once the bot is running, you can enter commands to manage your contacts. Here are the supported commands:

 - **add** <name> <phone>: Add a new contact with the given name and phone number.
 - **add-phone** <name> <phone>: Add a new phone number to the existing contact.
 - **add-birthday** <name> <birthday>: Add a birthday in DD.MM.YYYY format to the existing contact.
 - **all**: View all contacts and their phone numbers.
 - **birthdays**: View this week's upcoming birthdays.
 - **delete** <name>: Remove the specific contact from the contact book.
 - **change** <name> <old_phone> <new_phone>: Change the phone number of an existing contact to a new one.
 - **exit** or **close**: Exit the bot.
 - **phone** <name>: Retrieve the phone numbers of a specific contact.
 - **hello**: Greet the bot and get assistance.
 - **show-birthday** <name>: Show the birthday of the existing contact.
 - **remove** <name>: Remove the specific contact from the contact book.

After stopping bot saves its current state to your home directory in the `.ConsoleBot` directory, `bot_data.json` file in JSON format. When the bot is started again, it will try to restore all data from this file.  

 
