from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from core.config.enums.BotTgCommands import BotTgCommands
BotDispatcher = Dispatcher()

@BotDispatcher.callback_query()
async def test():
  print('callback_query')