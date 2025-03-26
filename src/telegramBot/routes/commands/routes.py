from modules.users.usersRepository import AccountRepository
from telegramBot import (
    BotDispatcher,
    BotTgCommands,
)
from aiogram.filters import Command
from aiogram.types import (
    Message,
)

@BotDispatcher.message(Command(commands=BotTgCommands.START.value))
async def start(message: Message):
    tg_id = message.from_user.id
    if not tg_id: return
    user = await AccountRepository.getOrCreateUserById(tg_id)
    await message.answer(text="Спасибо что пользуетесь нашим приложением")

# @BotDispatcher.message(F.text.regexp(r"^[+-]\s*\d+(\.\d+)?"))
# async def inline_operations(message: Message):
#     userid = message.from_user.id
#     user = await UserRepository.getUserById(userid)
#     sign, summ, category = message.text.split(" ")[0:3]
