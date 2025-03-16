from core import KeyboardButtons, BotTgCommands
from aiogram.filters import BaseFilter
from aiogram.types.message import Message


class IsReplyButtonFilter(BaseFilter):
    def __init__(self, keyboardType: BotTgCommands):
        self.keyboardType = keyboardType

    def findButtonInKeyboard(self, buttonText: str):
        if not self.keyboardType:
            return False
        keyboard = KeyboardButtons[self.keyboardType]
        if not keyboard or len(keyboard) == 0:
            return False
        for row in keyboard:
            for button in row:
                if button.text == buttonText:
                    return True

        return False

    async def __call__(self, message: Message):
        validKeyboard = self.findButtonInKeyboard(message.text)
        if not validKeyboard:
            return False
        return True
