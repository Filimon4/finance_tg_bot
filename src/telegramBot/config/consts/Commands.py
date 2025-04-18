from ..enums.BotTgCommands import BotTgCommands
from aiogram.types import BotCommand

Commands = {
    BotCommand(
        command=f"/{BotTgCommands.START.value}", description="Запуск бота"
    ),
    BotCommand(
        command=f'/{BotTgCommands.EXPORT.value}', description="Експорт данных за послдение месяцы"
    ),
    # BotCommand(
    #     command=f'/{BotTgCommands.CHECK_ALL_REMINDERS.value}', description="Експорт данных за послдение месяцы"
    # ),
    # BotCommand(
    #     command=f'/{BotTgCommands.UPDTATE_CURRENCY.value}', description="Обновить все валюты и курсы"
    # ),
    # BotCommand(
    #     command=f'/{BotTgCommands.UPDTATE_ALL_CURRENCY.value}', description="Обновить все валюты"
    # ),
    # BotCommand(
    #     command=f'/{BotTgCommands.UPDATE_CURRENCY_RATES.value}', description="Обновить все курсы"
    # ),
    # BotCommand(
    #     command=f'/{BotTgCommands.ALL_THIRD_APIS.value}', description="Список внешних api"
    # ),
    # BotCommand(
    #     command=f'/{BotTgCommands.API_STATUS.value}', description="Статус api"
    # ),
    BotCommand(
        command=f'/{BotTgCommands.HELP.value}', description="Помощь"
    )
}
