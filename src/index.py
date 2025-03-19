import asyncio
import os
from db import DB

from core import MainBotTg, BotDispatcher
from utils.loadModulesByRegex import load_modules_by_regex


async def main():
    await MainBotTg.set_default_command()
    await BotDispatcher.start_polling(MainBotTg)


if __name__ == "__main__":
    print("Запуск бота")
    load_modules_by_regex(os.path.dirname("src/"), r"routes.py")
    asyncio.run(main())
