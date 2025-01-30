import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from core import MainBotTg, BotDispatcher

from utils.loadModulesByRegex import load_modules_by_regex
load_modules_by_regex(os.path.dirname('src/routes'), r'routes.py')

async def main():
    print()
    await MainBotTg.set_default_command()
    await BotDispatcher.start_polling(MainBotTg)

if __name__ == "__main__":
    asyncio.run(main())
