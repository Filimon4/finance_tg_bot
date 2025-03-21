from ..enums.BotTgCommands import BotTgCommands
from aiogram.types import BotCommand

Commands = {
    BotCommand(
        command=f"/{BotTgCommands.START.value}", description="Запуск бота"
    ),
}
