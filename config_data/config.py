from dataclasses import dataclass

from environs import Env

@dataclass
class TgBot:
    token: str #Token for access to the telegram bot
    admin_ids: list[int] #List of bot administrator IDs

@dataclass
class Config:
    tg_bot: TgBot

# Create a function that will read the .env file and return 
# an instance of the Config class with the token and admin_ids fields filled in
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot = TgBot(
            token = env('BOT_TOKEN'),
            admin_ids= list(map(int, env.list('ADMIN_IDS')))
        )
    )