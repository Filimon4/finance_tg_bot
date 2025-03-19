from core import BotDispatcher
from aiogram import F, Router
from aiogram.types import Message
from ..users.users_repository import UserRepository

operations_router = Router(name="operations_router")
BotDispatcher.include_router(operations_router)


@operations_router.message(F.text.regexp(r"^[+-]\s*\d+(\.\d+)?"))
async def inline_operations(message: Message):
    userid = message.from_user.id
    sign, summ, category = message.text.split(" ")[0:3]
    user = await UserRepository.getUserById(userid)
