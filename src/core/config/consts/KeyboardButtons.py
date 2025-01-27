from ..enums.BotTgCommands import BotTgCommands
from aiogram.types import KeyboardButton

KeyboardButtons = {
  BotTgCommands.START: [
    [
      KeyboardButton(text="Нажми меня"),
      KeyboardButton(text="Нажми меня тоже")
    ]
  ]
}
