import os
from aiogram import Bot

from src.telegramBot.config.consts.Commands import Commands


class BotTg(Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def set_default_command(self):
        await self.set_my_commands(Commands)


TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения 'BOT_TOKEN' не найдена!")
MainBotTg = BotTg(token=TOKEN)
