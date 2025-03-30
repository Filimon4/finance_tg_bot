import asyncio
import os

from src.telegramBot import MainBotTg, BotDispatcher
from src.utils.loadModulesByRegex import load_modules_by_regex
import src.telegramBot.routes.commands.routes

async def main():
    await MainBotTg.set_default_command()
    await BotDispatcher.start_polling(MainBotTg)


if __name__ == "__main__":
    print("Запуск бота")
    # load_modules_by_regex(os.path.dirname("./src/telegramBot"), r"routes.py")
    asyncio.run(main())
