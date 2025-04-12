from enum import Enum


class BotTgCommands(Enum):
    START = "start"
    HELP = "help"
    EXPORT = "export"
    CHECK_ALL_REMINDERS = "check_all_reminders"
    UPDTATE_CURRENCY = "update_currency"
    UPDATE_ONE_CURRENCY = "update_currency_rate"