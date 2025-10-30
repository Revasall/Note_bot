# Note Bot — Telegram bot for taking notes

Note Bot is a Telegram bot that allows users to create notes, attach various files, edit and organize them into groups, and effectively organize personal notes.

The project demonstrates skills in working with bots, asynchronous event processing, data storage, and state management.

![Note Bot icon](https://github.com/Revasall/Note_bot/blob/main/media_readme/2aa24615-82f6-47b2-9c2a-5d70a2b3940d.png?raw=true)


## Features

- __CRUD operations notes with the ability to attach media files__
  - CRUD operations are performed using a message and the inline keyboard in the Telegram bot.
  - Each note can contain a photo, video, or document, as well as a list of texts sent in multiple messages.
  - The database stores the file code in the Telegram, not the file itself.
  
- __Creating, editing, and deleting note groups__
  - CRUD operations are also performed through the bot's dialog and keyboard. A group is a list of notes that the user selects from existing ones.
  - The bot allows editing this list and displaying all the notes it contains at once.

- __Data Base__
  - The PostgreSQL database is used, as well as SQLAlchemy for working with it in Python.
  - Two related tables, Notes and Groups, are used to store notes and groups.
  
- __Interactive user interaction with the inlinekeyboards/menus__
  - To work with the bot, several inline keyboards have been implemented, a common menu-keyboard, and pagination is present when selecting notes for adding and editing in a group
    
- __Using , states, and filters__
  - To operate the bot, two state classes have been implemented for a note and a group, through which complex logic of interaction with the bot is implemented

### Future features
- In the future, we plan to migrate from the state system to Redis, which will allow for more secure storage of user information.

- Pagination will be added for selecting large numbers of groups.

- Adding Middleware

- Adding English language support for the bot (Russian is not used).

## Technologies

- Python 3.12.6
- Aiogram 3.17.0
- SQLAlchemy 2.0,
- PostgreSQL + asyncpg

Other libraries and technologies used can be found in requirements.txt.

## Installation and launch
Downloading the project:
git clone https://github.com/Revasall/Note_bot.git
cd Note_bot
python -m venv .venv

source .venv/bin/activate      # для Linux/macOS
# или .venv\Scripts\activate   # для Windows
source .venv/Scripts/activate #для bush

pip install -r requirements.txt
python main.py

```git clone https://github.com/Revasall/Note_bot.git```

```cd Note_bot```

Setting up the environment:
```python -m venv .venv```

```
source .venv/bin/activate      # for Linux/macOS
.venv\Scripts\activate   # for Windows
source .venv/Scripts/activate # for bush
```

```pip install -r requirements.txt```

Create a database in PostgreSQL
Configure the .env file as in .env.example
Request a token from BotFather for the bot and add it to the BOT_TOKEN line in .env

```python main.py```

Open the bot in Telegram and start working.



## Author 

Macvej Reut 

Python backend developer

Philosopher and logician



📧 Email: [matvejreut@gmail.com]

🐙 GitHub: [https://github.com/Revasall]


