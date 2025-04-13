from enum import Enum


class BotTgCommands(Enum):
    START = "start"
    HELP = "help"
    EXPORT = "export"
    CHECK_ALL_REMINDERS = "check_all_reminders"
    UPDTATE_ALL_CURRENCY = "updtate_all_currency"
    UPDTATE_CURRENCY = "update_currency"
    UPDATE_CURRENCY_RATES = "update_currency_rates"
    ALL_THIRD_APIS = "all_third_apis"
    API_STATUS = "api_status"