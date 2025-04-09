import datetime
import re
from aiogram import F

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
    MainBotTg
)
from aiogram.filters import Command
from aiogram.types import (
    Message,
    BufferedInputFile
)
from sqlalchemy.exc import SQLAlchemyError


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
        matched = re.match(r'^(\/export)\s+(\d+)$', text)
        if not matched:
            await message.answer(text='Неправильный шаблон команды. Пример использования: /export 12')
            return

        _, month = matched.groups()
        month = int(month)
        await message.answer(f'🔍 Формирую отчет за {month} месяцев...')

        with DB.get_session() as session:
            await ExcelReportGenerator.generate_and_send_report(
                message=message,
                month=month,
                user_id=user_id,
                session=session
            )

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        await message.answer(text="❌ Ошибка базы данных при экспорте")
    except Exception as e:
        print(f"Export error: {e}")
        await message.answer(text="❌ Произошла ошибка при формировании отчета")
# async def export(message: Message):
#     try:
#         user_id = message.from_user.id
#         text = message.text.strip()
#         matched = re.match(r'^(\/export)\s+(\d+)$', text)
#         if not matched:
#             await message.answer(text='Неправильный шаблон команды. Пример использования: /export 12')
#             return

#         command, month = matched.groups()
#         month = int(month)
#         await MainBotTg.send_message(text=f'Экспорт данных за {month} мес.', chat_id=message.chat.id)
        
#         with DB.get_session() as session:
#             end_time = datetime.datetime.now()
#             start_time = end_time - datetime.timedelta(days=30*month)

#             report_generator = ExcelReportGenerator(report_file=f"exel_report_{user_id}.xlsx")
            
#             with DB.get_session() as session:
#                 report_path = report_generator.generate_operations_report(session, user_id, start_time, end_time)
            
#             with open(report_path, 'rb') as file:
#                 file_content = file.read()
            
#             input_file = BufferedInputFile(
#                 file=file_content,
#                 filename=f"report_{month}_months.xlsx"
#             )
#             report_generator.cleanup()
            
#             await message.answer_document(document=input_file, caption=f"Отчет за {month} месяцев")
#     except SQLAlchemyError as e:
#         print(e)
#         await message.answer(text="Произошла ошибка при экспорте данных")
#     except Exception as e:
#         print(e)
#         await message.answer(text="Произошла ошибка при экспорте данных")

        

@BotDispatcher.message(F.text.regexp(r"^[+-]\s*\d+(\.\d+)?"))
async def inline_operations(message: Message):
    try:
        userid = message.from_user.id
        with DB.get_session() as session:
            sign, amount, category = message.text.split(" ")[0:3]
            user = AccountRepository.getUserById(session, userid)
            category = CategoryRepository.getByName(session, user.id, category)
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
        return
    except SQLAlchemyError as e:
        await message.answer(text=f"Ошибка при добавлении операции")
    except Exception as e:
        await message.answer(text=f"Ошибка при добавлении операции")