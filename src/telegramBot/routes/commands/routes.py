from asyncio.log import logger
import json
import re
from aiogram import F
from src.modules.currency.index import CurrencyEnum
from src.modules.excelReportGenerator.index import ExcelReportGenerator
from src.modules.finance.types import OperationType
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.categories.catogoriesRepository import CategoryRepository
from src.modules.finance.operations.operationsRepository import OperationCreateDTO, OperationsRepository
from src.db.index import DB
from src.modules.accounts.accountsRepository import AccountRepository
from src.telegramBot import (
    BotDispatcher,
    BotTgCommands,
    Reminder
)
from aiogram.filters import Command
from aiogram.types import (
    Message,
    WebAppData,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from sqlalchemy.exc import SQLAlchemyError

from src.telegramBot.system.currency.index import CurrencySys
from src.telegramBot.config.consts.KeyboardButtons import InlineKeyboardButtons, KeyboardButtons


@BotDispatcher.message(Command(commands=BotTgCommands.START.value))
async def start(message: Message):
    tg_id = message.from_user.id
    if not tg_id:
        return
    with DB.get_session() as session:
        AccountRepository.getOrCreateUserById(session, tg_id)
    await message.answer(text="Спасибо что пользуетесь нашим приложением")

@BotDispatcher.message(Command(commands=BotTgCommands.EXPORT.value))
async def export(message: Message):
    try:
        user_id = message.from_user.id
        text = message.text.strip()
        if not user_id or len(text) <= 0:
            raise Exception('Invalid user_id or text')
        await ExcelReportGenerator.on_command_export(user_id, text)
    except Exception as e:
        await message.answer(text="Ошибка при экспорте данных")

@BotDispatcher.message(F.text.regexp(r"^[+-]\s*\d+(\.\d+)?"))
async def inline_operations(message: Message):
    try:
        userid = message.from_user.id
        with DB.get_session() as session:
            sign, amount, category = message.text.split(" ")[0:3]
            user = AccountRepository.getUserById(session, userid)
            category = CategoryRepository.getByName(session, category)
            cashAccount = CashAccountRepository.getMain(session, user.id)

            data = OperationCreateDTO(
                account_id=user.id,
                amount=amount,
                category_id=category.id,
                cash_account_id=cashAccount.id,
                description='',
                name='',
                type=OperationType.INCOME if sign == '+' else OperationType.EXPENSIVE,
                to_cash_account_id=None,
            )
            operation = OperationsRepository.create(session,data)
            if not operation: raise Exception('Faile to create operation')

        await message.answer(text='Операция была добавленна')
    except SQLAlchemyError as e:
        await message.answer(text=f"Ошибка при добавлении операции")
    except Exception as e:
        await message.answer(text=f"Ошибка при добавлении операции")


@BotDispatcher.message(Command(commands=BotTgCommands.CHECK_ALL_REMINDERS.value))
async def send_all_reminders(message: Message):
    try:
        await Reminder.startFetching()
        await message.answer(text='Все напоминания обновлены')
    except SQLAlchemyError as e:
        await message.answer(text=f"Ошибка проверки напоминаний")
    except Exception as e:
        await message.answer(text=f"Ошибка проверки напоминаний")

@BotDispatcher.message(Command(commands=BotTgCommands.UPDTATE_ALL_CURRENCY.value))
async def update_all_currency(message: Message):
    try:
        await message.answer(text='Обновляем все валюты и курсы...')
        CurrencySys.updateAllApi()
    except SQLAlchemyError as e:
        await message.answer(text=f"Ошибка обновления валют")
    except Exception as e:
        await message.answer(text=f"Ошибка обновления валют")

@BotDispatcher.message(Command(commands=BotTgCommands.UPDTATE_CURRENCY.value))
async def update_currency(message: Message):
    try:
        args = message.text.strip().split(" ")
        if len(args) <= 1:
            await message.answer(text="Не указан api")
            text = "\n".join(CurrencyEnum.get_list())
            await message.answer(text=f"Список всех API: \n{text}")
            return
        api_type=args[1]
        await message.answer(text='Обновляем валюты...')
        CurrencySys.updateApiCurrencies(api_type)
        await message.answer(text=f"Обновление валюты {api_type} завершено")
    except SQLAlchemyError as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка обновления валют")
    except Exception as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка обновления валют")

@BotDispatcher.message(Command(commands=BotTgCommands.UPDATE_CURRENCY_RATES.value))
async def update_currency_rates(message: Message):
    try:
        args = message.text.strip().split(" ")
        if len(args) <= 1:
            await message.answer(text="Не указан api")
            text = "\n".join(CurrencyEnum.get_list())
            await message.answer(text=f"Список всех API: \n{text}")
            return
        api_type=args[1]
        await message.answer(text='Обновляем курсы валют...')
        CurrencySys.updateApiRates(api_type)
        await message.answer(text=f"Курсы валют {api_type} обновлены")
    except SQLAlchemyError as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка обновления курсов")
    except Exception as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка обновления курсов")

@BotDispatcher.message(Command(commands=BotTgCommands.ALL_THIRD_APIS.value))
async def send_all_apies(message: Message):
    try:
        text = "\n".join(CurrencyEnum.get_list())
        await message.answer(text=f"Список всех API: \n{text}")
    except SQLAlchemyError as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка отправки всех apis")
    except Exception as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка отправки всех apis")

@BotDispatcher.message(Command(commands=BotTgCommands.API_STATUS.value))
async def send_api_status(message: Message):
    try:
        args = message.text.strip().split(" ")
        if len(args) <= 1:
            await message.answer(text="Не указан api")
            text = "\n".join(CurrencyEnum.get_list())
            await message.answer(text=f"Список всех API: \n{text}")
            return
        api_type = args[1]
        text = CurrencySys.getApiStatus(api_type)
        await message.answer(text=f"Статус {api_type}: \n{text}")
    except SQLAlchemyError as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка отправки всех api статусов")
    except Exception as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка отправки всех api статусов")


@BotDispatcher.message(Command(commands=BotTgCommands.HELP.value))
async def send_help(message: Message):
    try:
        # TODO: Поменять когда добавится панель админа
        help_text = (
            "🤖 <b>Доступные команды:</b>\n\n"
            "🔹 /start — Запуск бота и приветственное сообщение\n"
            "🔹 /help — Показать это сообщение помощи\n"
            "🔹 /export — Экспортировать данные\n"
            # "🔹 /check_all_reminders — Проверка всех напоминаний\n"
            # "🔹 /updtate_all_currency — Обновить все валюты (есть опечатка в названии)\n"
            # "🔹 /update_currency — Обновить конкретную валюту\n"
            # "🔹 /update_currency_rates — Обновить курсы валют\n"
            # "🔹 /all_third_apis — Показать все сторонние API\n"
            # "🔹 /api_status — Проверить статус API\n\n"
            "ℹ️ Все команды можно вызывать с символом '/' в начале.\n"
        )

        buttons = InlineKeyboardButtons[BotTgCommands.HELP]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(text=help_text, parse_mode="HTML", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка в команде помощи")

@BotDispatcher.callback_query()
async def handle_callback(callback_query: CallbackQuery):
    data = callback_query.data

    print(data)
    
    await callback_query.answer()