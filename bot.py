import asyncio
from asyncio.log import logger
import os

import src.db.index
from src.telegramBot import MainBotTg, BotDispatcher
import src.telegramBot.routes.commands.routes

async def main():
    await MainBotTg.set_default_command()
    await BotDispatcher.start_polling(MainBotTg)


if __name__ == "__main__":
    logger.info('-- Start Bot')
    asyncio.run(main())
