from core import BotDispatcher, BotTgCommands, KeyboardButtons, IsReplyButtonFilter, MainBotTg
from aiogram.filters import Command
from aiogram import F
from aiogram.types import CallbackQuery,Message,ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton,User,MaybeInaccessibleMessage

@BotDispatcher.message(Command(commands=BotTgCommands.START.value))
async def start(message: Message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=KeyboardButtons[BotTgCommands.START], is_persistent=True)
  await message.answer(text='start command', reply_markup=keyboard)


@BotDispatcher.message(IsReplyButtonFilter(BotTgCommands.START))
async def reply(message: Message):
  await message.answer(text='reply command')

@BotDispatcher.message(F.text == 'inline')
async def inline_message(message: Message):
  inlineKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(text='inline 1', callback_data='1'),
      InlineKeyboardButton(text='inline 2', callback_data='2'),
    ]
  ])
  await message.answer(text='inline', reply_markup=inlineKeyboard)

@BotDispatcher.callback_query(lambda x: x.data == '1')
async def callback_query_handler(callback_query: CallbackQuery):
  print('Data 1: ', callback_query.id, callback_query.from_user.id, callback_query.data)
  await MainBotTg.answer_callback_query(
    callback_query_id=callback_query.id, 
    text='callback_query_handler',
  )
@BotDispatcher.callback_query(lambda x: x.data == '2')
async def callback_query_handler(callback_query: CallbackQuery):
  print('Data 2: ', callback_query.id, callback_query.from_user.id, callback_query.data)
  await MainBotTg.answer_callback_query(
    callback_query_id=callback_query.id, 
    text='callback_query_handler',
  )