from core import BotDispatcher, BotTgCommands, KeyboardButtons, IsReplyButtonFilter
from aiogram.filters import Command
from aiogram.types import Message,ReplyKeyboardMarkup

@BotDispatcher.message(Command(commands=BotTgCommands.START.value))
async def start(message: Message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=KeyboardButtons[BotTgCommands.START], is_persistent=True)
  await message.answer(text='start command', reply_markup=keyboard)


@BotDispatcher.message(IsReplyButtonFilter(BotTgCommands.START))
async def reply(message: Message):
  await message.answer(text='reply command')