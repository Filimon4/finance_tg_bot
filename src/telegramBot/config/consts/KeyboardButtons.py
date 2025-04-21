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
  ],
  "admin": [
    [InlineKeyboardButton(text="Проверить все напоминания", callback_data="check_all_reminders")],
    [
      InlineKeyboardButton(text="Обновить все валюты и курсы", callback_data="update_currency"),
      InlineKeyboardButton(text="Обновить все валюты", callback_data="update_all_currency"),
      InlineKeyboardButton(text="Обновить все курсы", callback_data="update_currency_rates")
    ],
    [
      InlineKeyboardButton(text="Список внешних api", callback_data="all_third_apis"),
      InlineKeyboardButton(text="Статус api", callback_data="api_status")
    ],
  ]
}
