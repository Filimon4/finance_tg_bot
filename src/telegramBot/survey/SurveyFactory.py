from aiogram import Router
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.telegramBot import BotDispatcher

class SurveyFactory:
    def __init__(self, chatId: int, firstState: State):
        self.first_state = firstState
        self.chat_id = chatId
        self.router = Router()
        BotDispatcher.include_router(self.router)

    async def start(self, state: FSMContext):
        await state.set_state(self.first_state)

    async def cancel_survey(self, message: Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            await message.answer("Нет активного опроса.")
            return
        
        await state.clear()
        await message.answer("Опрос отменен.", reply_markup=ReplyKeyboardRemove())

    async def complete_survey(self, state: FSMContext):
        user_data = await state.get_data()
        await state.clear()
        return user_data