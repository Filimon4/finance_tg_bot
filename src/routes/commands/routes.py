from core import BotDispatcher, BotTgCommands, KeyboardButtons
from aiogram.filters import Command
from aiogram.types import Message,ReplyKeyboardMarkup

@BotDispatcher.message(Command(commands=BotTgCommands.START.value))
async def start(message: Message):
  # Создаём клавиатуру
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=KeyboardButtons[BotTgCommands.START], is_persistent=True)
  
  await message.answer(text='start command', reply_markup=keyboard)
