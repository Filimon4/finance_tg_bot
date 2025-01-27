import os
from aiogram import Bot
from aiogram.types import BotCommand
from core.config.enums.BotTgCommands import BotTgCommands

class BotTg(Bot):
  commands = [
    BotCommand(command=f"/{BotTgCommands.START.value}", description="Запуск бота"),
  ]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  async def set_default_command(self):
    await self.set_my_commands(BotTg.commands)
    

TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("Переменная окружения 'BOT_TOKEN' не найдена!")
MainBotTg = BotTg(token=TOKEN)
