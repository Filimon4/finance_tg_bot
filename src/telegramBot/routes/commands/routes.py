from asyncio.log import logger
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
    Reminder,
    MainBotTg
)
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from src.telegramBot.system.currency.index import CurrencySys
from src.telegramBot.config.consts.KeyboardButtons import InlineKeyboardButtons
from src.telegramBot.survey import ApiStatusSurvey, CurrencyUpdateSurvey, RateUpdateSurvey 

@BotDispatcher.message(Command(commands=BotTgCommands.START.value))
async def start(message: Message):
    tg_id = message.from_user.id
    if not tg_id:
        return
    isAdmin = False
    with DB.get_session() as session:
        user = AccountRepository.getOrCreateUserById(session, tg_id)
        if user.admin == True:
            isAdmin = True

    if isAdmin:
        buttons = InlineKeyboardButtons["admin"]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(text="Привет Админ", reply_markup=keyboard)
    else:
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
            values = message.text.split(" ")[0:3]
            sign, amount, *rest = values
            user = AccountRepository.getUserById(session, userid)
            cashAccount = CashAccountRepository.getMain(session, user.id)
            category = None

            if len(rest) >= 1 and rest[0]:
                category = CategoryRepository.getByName(session, user.id, rest[0])
                if not category:
                    await message.answer(text='Категория была не найдена')


            data = OperationCreateDTO(
                account_id=user.id,
                amount=amount,
                category_id=category.id if category is not None else None,
                cash_account_id=cashAccount.id,
                description='',
                name='',
                type=OperationType.INCOME if sign == '+' else OperationType.EXPENSIVE,
                to_cash_account_id=None,
                date=str(datetime.now())
            )
            operation = OperationsRepository.create(session,data)
            if not operation: raise Exception('Faile to create operation')

        await message.answer(text='Операция была добавленна')
    except SQLAlchemyError as e:
        await message.answer(text=f"Ошибка при добавлении операции")
    except Exception as e:
        print(e)
        await message.answer(text=f"Ошибка при добавлении операции")

async def send_all_reminders(chatId: int):
    try:
        await Reminder.startFetching()
        await MainBotTg.send_message(text='Все напоминания обновлены', chat_id=chatId)
    except SQLAlchemyError as e:
        await MainBotTg.send_message(text=f"Ошибка проверки напоминаний")
    except Exception as e:
        await MainBotTg.send_message(text=f"Ошибка проверки напоминаний")

async def update_all_currency(chatId: int):
    try:
        await MainBotTg.send_message(text='Обновляем все валюты и курсы...', chat_id=chatId)
        CurrencySys.updateAllApi()
    except SQLAlchemyError as e:
        await MainBotTg.send_message(text=f"Ошибка обновления валют")
    except Exception as e:
        await MainBotTg.send_message(text=f"Ошибка обновления валют")

async def update_currency(chatId: int, state: FSMContext):
    try:
        surveyEntity = CurrencyUpdateSurvey(chat_id=chatId)
        await surveyEntity.start(state)
    except SQLAlchemyError as e:
        logger.error(f"{str(e)}")
        await MainBotTg.send_message(text=f"Ошибка обновления валют")
    except Exception as e:
        logger.error(f"{str(e)}")
        await MainBotTg.send_message(text=f"Ошибка обновления валют")

async def update_currency_rates(chatId: int, state: FSMContext):
    try:
        surveyEntity = RateUpdateSurvey(chat_id=chatId)
        await surveyEntity.start(state)
    except SQLAlchemyError as e:
        logger.error(f"{str(e)}")
        await MainBotTg.send_message(text=f"Ошибка обновления курсов")
    except Exception as e:
        logger.error(f"{str(e)}")
        await MainBotTg.send_message(text=f"Ошибка обновления курсов")

async def send_all_api(chatId: int):
    try:
        text = "\n".join(CurrencyEnum.get_list())
        await MainBotTg.send_message(text=f"Список всех API: \n{text}", chat_id=chatId)
    except SQLAlchemyError as e:
        logger.error(f"{str(e)}")
        await MainBotTg.send_message(text=f"Ошибка отправки всех apis")
    except Exception as e:
        logger.error(f"{str(e)}")
        await MainBotTg.send_message(text=f"Ошибка отправки всех apis")

async def send_api_status(chatId: int, state: FSMContext):
    try:
        surveyEntity = ApiStatusSurvey(chatId)
        await surveyEntity.start(state)
    except SQLAlchemyError as e:
        logger.error(f"{str(e)}")
        await MainBotTg.send_message(text=f"Ошибка отправки всех api статусов", chat_id=chatId)
    except Exception as e:
        logger.error(f"{str(e)}")
        await MainBotTg.send_message(text=f"Ошибка отправки всех api статусов", chat_id=chatId)


@BotDispatcher.message(Command(commands=BotTgCommands.HELP.value))
async def send_help(message: Message):
    try:
        help_text = (
            "🤖 <b>Доступные команды:</b>\n\n"
            "🔹 /start — Запуск бота и приветственное сообщение\n"
            "🔹 /help — Показать это сообщение помощи\n"
            "🔹 /export — Экспортировать данные\n"
            "ℹ️ Все команды можно вызывать с символом '/' в начале.\n"
        )

        buttons = InlineKeyboardButtons[BotTgCommands.HELP]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await message.answer(text=help_text, parse_mode="HTML", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"{str(e)}")
        await message.answer(text=f"Ошибка в команде помощи")

@BotDispatcher.callback_query(
    ~F.data.in_(CurrencyEnum.get_list())
)
async def handle_callback(callback_query: CallbackQuery, state: FSMContext):
    data = callback_query.data
    userId = callback_query.from_user.id
    
    if data == "check_all_reminders":
        await send_all_reminders(chatId=userId)
    elif data == "update_currency":
        await update_currency(chatId=userId, state=state)
    elif data == "update_all_currency":
        await update_all_currency(chatId=userId)
    elif data == "update_currency_rates":
        await update_currency_rates(chatId=userId, state=state)
    elif data == "all_third_apis":
        await send_all_api(chatId=userId)
    elif data == "api_status":
        await send_api_status(chatId=userId, state=state)

    await callback_query.answer()