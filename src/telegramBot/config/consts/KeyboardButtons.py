from ..enums.BotTgCommands import BotTgCommands
from aiogram.types import KeyboardButton, InlineKeyboardButton, WebAppInfo

KeyboardButtons = {
    BotTgCommands.START: [
      
    ]
}

InlineKeyboardButtons = {
  BotTgCommands.START: [
    [InlineKeyboardButton(text="Панель админа", callback_data='admin_panel')]
  ],
  BotTgCommands.HELP: [
        [InlineKeyboardButton(text="Открыть приложение", web_app=WebAppInfo(url="https://finance-tg-miniapp.netlify.app")),]
    ]
}
