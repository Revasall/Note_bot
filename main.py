import asyncio 
import logging 

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu

from database.models import async_models_main


# Initialize the logger
logger = logging.getLogger(__name__)

# Function of configuring and launching the bot
async def main():
     # Configure logging
     logging.basicConfig(
          level=logging.INFO,
          format='%(filename)s:%(lineno)d #%(levelname)-8s '
                 '[%(asctime)s] - %(name)s - %(message)s'
                 )
     
     #Output to console information about the start of the bot launch
     logger.info('Starting bot')

     #Create Databases
     await async_models_main()
     logger.info('Starting database')

     #loading dataclass Config into variable config
     config: Config = load_config()

     #Initializing the storage
     storage = MemoryStorage()

     #Initialization of the bot and dispatcher
     bot = Bot(
          token=config.tg_bot.token,
          default= DefaultBotProperties(parse_mode=ParseMode.HTML))
     dp = Dispatcher(storage=storage )
     logger.info('Initializatein bot')

     #Configuring the main menu
     logger.info('Loading main menu')
     await set_main_menu(bot)

     # Registering handlers in the dispatcher
     logger.info('Loading handlers into the dispatcher')
     dp.include_router(user_handlers.router)
     dp.include_router(other_handlers.router)

     #Skipping accumulated updates and starting pooling
     await bot.delete_webhook(drop_pending_updates=True)
     await dp.start_polling(bot)

asyncio.run(main())



