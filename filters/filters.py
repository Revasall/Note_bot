from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

class IsDelNoteCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('bot_del')
    
class IsEditNoteCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('bot_edit')
    