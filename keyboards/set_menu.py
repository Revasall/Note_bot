from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_ru import LEXICON_COMMANDS

#Function for customizing the menu
async def set_main_menu(bot: Bot): 
    main_menu_command = [BotCommand(
        command=command,
        description=description)
        for command, description in LEXICON_COMMANDS.items()
        ]
    
    await bot.set_my_commands(main_menu_command)