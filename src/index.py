import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
from db import DB

from core import MainBotTg, BotDispatcher
from utils.loadModulesByRegex import load_modules_by_regex


async def main():
    print()
    await MainBotTg.set_default_command()
    await BotDispatcher.start_polling(MainBotTg)


if __name__ == "__main__":
    print("Запуск бота")
    load_modules_by_regex(
        os.path.dirname("src/routes"), r"routes.py"
    )  # авто-загрузка всех routes приложения
    asyncio.run(main())
