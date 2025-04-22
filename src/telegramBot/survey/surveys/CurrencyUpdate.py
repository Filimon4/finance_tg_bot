from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from src.modules.currency.index import CurrencyEnum
from src.telegramBot.system.currency.index import CurrencySys
from ..SurveyFactory import SurveyFactory
from src.telegramBot import MainBotTg
from aiogram import F

class CurrencyUpdateStatusGroup(StatesGroup):
  api_type = State()

class CurrencyUpdateSurvey(SurveyFactory):
  
  def __init__(self, chat_id):
    super().__init__(chat_id, CurrencyUpdateStatusGroup.api_type)
    self.registerHandlers()

  def registerHandlers(self):
    @self.router.callback_query(CurrencyUpdateStatusGroup.api_type)
    async def apiTypeCallback(callback_query: CallbackQuery, state: FSMContext):
      await state.update_data(api_type=callback_query.data)
      user_data = await self.complete_survey(state)
      await callback_query.answer()
      if user_data['api_type']:
        api_type = user_data['api_type']
        await MainBotTg.send_message(self.chat_id, text=f"Обновление валют для {api_type}")
        CurrencySys.updateApiCurrencies(api_type)

  async def start(self, state: FSMContext):
    await super().start(state)
    buttons = [[InlineKeyboardButton(text=button, callback_data=button) for button in CurrencyEnum.get_list()]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await MainBotTg.send_message(self.chat_id, text='Выберете тип api', reply_markup=keyboard)