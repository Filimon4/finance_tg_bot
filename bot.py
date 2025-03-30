import asyncio
import os

import src.db.index
from src.telegramBot import MainBotTg, BotDispatcher
import src.telegramBot.routes.commands.routes

async def main():
    await MainBotTg.set_default_command()
    await BotDispatcher.start_polling(MainBotTg)


if __name__ == "__main__":
    print("Запуск бота")
    # load_modules_by_regex(os.path.dirname("./src/telegramBot"), r"routes.py")
    asyncio.run(main())
