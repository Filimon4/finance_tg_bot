from ..enums.BotTgCommands import BotTgCommands
from aiogram.types import BotCommand

Commands = {
    BotCommand(
        command=f"/{BotTgCommands.START.value}", description="Запуск бота"
    ),
    BotCommand(
        command=f'/{BotTgCommands.EXPORT.value}', description="Експорт данных за послдение месяцы"
    )
}
