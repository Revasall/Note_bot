from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
import database.requests as rq

from keyboards.keyboards_builder import static_keyboard


from lexicon.lexicon_ru import  LEXICON_MESSAGES, LEXICON_COMMANDS, LEXICON_BUTTONS


#router initialization
router = Router()


# ___________
# Start commands handlers
# ___________

# Handler processes /start. Sends a greeting, shows the keyboard, and logs the user in.
@router.message(StateFilter(default_state), CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON_COMMANDS[message.text], 
                         reply_markup=static_keyboard())
    await rq.set_user(message.from_user.id)

# The handler processes /help or the "Help" button and sends help to the user.
@router.message(StateFilter(default_state), Command(commands='help'))
@router.message(F.text == LEXICON_BUTTONS['help'], StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(LEXICON_MESSAGES['/help'])

# The handler processes /cancel and clears the FSM state, notifying the user.
@router.message(~StateFilter(default_state), Command(commands='cancel'))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_MESSAGES['cancel'])
    await state.clear()

# The handler processes the "Cancel" button and clears the FSM state by updating the message.
@router.callback_query(~StateFilter(default_state), F.data == 'cancel')
async def process_cancel_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_MESSAGES['cancel'])
    await state.clear()





