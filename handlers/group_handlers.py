from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from states.fsm_fill_form import GroupStates

from database import requests as rq
from services import services as serv
from utils.utils import CallbackPrefix
from keyboards.keyboards_builder import (select_notes_for_group_keyboard,
                                        groups_list_keyboard,
                                        group_keyboard)
from lexicon.lexicon_ru import LEXICON_MESSAGES, LEXICON_ERRORS, LEXICON_BUTTONS


router = Router()

#----------------------
# CREATE GROUP HANDLERS
# ---------------------

# Processes the /create_group command
# Goes to the awaiting_group_title state and waits for the user to enter a group title
@router.message(StateFilter(default_state), Command(commands='create_group'))
@router.message(StateFilter(default_state), F.text == LEXICON_BUTTONS['create_group'])
async def process_create_group_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_MESSAGES['create_group'])
    await state.set_state(GroupStates.awaiting_group_title)


# Handle group title input and move to text input
@router.message(StateFilter(GroupStates.awaiting_group_title), F.text)
async def process_group_title_sent(message: Message, state: FSMContext):
    if len(message.text) <= 200:
        note_list = await rq.get_note_titles(message.from_user.id)
        await state.update_data(title_group_note=message.text)
        await message.answer(
            text=LEXICON_MESSAGES['select_notes_for_group'],
            reply_markup=select_notes_for_group_keyboard(note_list)
        )
        await state.set_state(GroupStates.select_notes_to_add)
    else: 
        await message.answer(LEXICON_ERRORS['title_is_too_long'])

# If the message type is incorrect, sends the user a warning message about the incorrect note text
@router.message(StateFilter(GroupStates.awaiting_group_title))
async def notify_invalid_title(message: Message):
    await message.answer(LEXICON_ERRORS['invalid_title']) 



# Handler selects the attack to be given to the group.
@router.callback_query(StateFilter(GroupStates.select_notes_to_add), F.data.startswith(CallbackPrefix.SELECT))
async def process_note_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    note_list = await rq.get_note_titles(callback.from_user.id)
    group_data = await state.get_data()
    group_data['select_notes'] = group_data.get('select_notes', []) + [int(callback.data.split('_')[1])]
    await callback.message.edit_reply_markup(
        reply_markup=select_notes_for_group_keyboard(
            note_list,
            group_data['select_notes'])
            )
    await state.set_data(group_data)

# Delete the selected attachment from the group list and delete the keyboard.
# Kali element is not in the list, showing an alert to the mercenary.
@router.callback_query(StateFilter(GroupStates.select_notes_to_add), F.data.startswith(CallbackPrefix.DEL))
async def process_del_note_from_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    note_list = await rq.get_note_titles(callback.from_user.id)
    group_data = await state.get_data()
    
    try:
        group_data['select_notes'].remove(int(callback.data.split('_')[1]))
        await callback.message.edit_reply_markup(
        reply_markup=select_notes_for_group_keyboard(
            note_list,
            group_data['select_notes'])
            )
    except ValueError: 
        callback.answer(
            text=LEXICON_ERRORS['error_group_deleting'], 
            show_alert=True)

    await state.set_data(group_data)


# Completes the selection of notes for the group.
# If the selected list of notes is not empty, creates a new group or updates an existing one.
# Sends a message to the user about the result and clears the FSM state.
# If the list is empty or an error occurs, displays an alert.
@router.callback_query(StateFilter(GroupStates.select_notes_to_add), F.data == 'finish_selection')
async def complete_selection(callback: CallbackQuery, state: FSMContext):
    group_data = await state.get_data()

    try:
        notes = group_data.get('select_notes')
        if not notes: 
            await callback.answer(text=LEXICON_MESSAGES['no_select_note'])
            return
        
        # Create a new group
        if 'title_group_note' in group_data:
            await rq.set_group(group_data['title_group_note'], group_data['select_notes'], callback.from_user.id)
            await callback.message.edit_text(LEXICON_MESSAGES['group_created'])
            await state.clear()

        #Update an existing group
        if 'group_id' in group_data:
            await rq.update_notes_in_group(group_data['group_id'], group_data['select_notes'])
            await callback.message.edit_text(LEXICON_MESSAGES['group_updated'])
            await state.clear()
    except:
        await callback.answer(text=LEXICON_ERRORS['error_group_creationg'])
    


#----------------------
# SELECT GROUP HANDLERS
# ---------------------



# The handler starts the group selection process.
# If the user has groups — shows a list with a keyboard and goes to the corresponding FSM state.
# If there are no groups — sends a message that there are no groups.
@router.message(StateFilter(default_state), Command(commands='select_group'))
@router.message(StateFilter(default_state), F.text == LEXICON_BUTTONS['select_group'])
async def start_select_group(message: Message, state: FSMContext):
    groups = await rq.get_group_titles(message.from_user.id)
    if len(list(groups))>0:
        await message.answer(
            text=LEXICON_MESSAGES['select_group'],
            reply_markup=groups_list_keyboard(groups, all_groups=False)
            )
        await state.set_state(GroupStates.select_group_to_view)
    else:
        await message.answer(LEXICON_MESSAGES['no_groups'])


# The handler shows the selected group.
# Gets the group id from callback.data, gets the data from the DB and edits the message,
# showing the group name and the corresponding keyboard.
@router.callback_query(StateFilter(GroupStates.select_group_to_view), F.data.startswith(CallbackPrefix.GROUP))
async def complete_send_group(callback: CallbackQuery, state: FSMContext):
    group_id = int(callback.data.split('_')[1])
    group_data = await rq.get_group(group_id)
    await callback.message.edit_text(
        text=group_data.title,
        reply_markup=(group_keyboard(group_id))
        )
    


#----------------------
# EDIT GROUP HANDLERS
# ---------------------



# Handler starts editing the group.
# Gets the group id from the callback, gets its notes, shows the keyboard with the selected notes,
# updates the FSM state and enters group editing mode.
@router.callback_query(StateFilter(GroupStates.select_group_to_view), F.data.startswith(CallbackPrefix.EDIT))
async def start_edit_group_notes_list(callback: CallbackQuery, state: FSMContext):
    group_id = int(callback.data.split('_')[1])
    group_data = await rq.get_group(group_id)

    notes = await rq.get_note_titles(callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON_MESSAGES['select_notes_for_group'],
        reply_markup=select_notes_for_group_keyboard(notes, group_data.notes_ls))
    
    await state.update_data(group_id=group_id, select_notes=group_data.notes_ls)
    await state.set_state(GroupStates.select_notes_to_add)


# The handler shows the group's "wall" of notes.
# Gets the group id from the callback, gets its notes, and sends them to the user.
# When finished, removes the keyboard and clears the FSM state.
@router.callback_query(StateFilter(GroupStates.select_group_to_view), F.data.startswith(CallbackPrefix.WALL))
async def process_notes_wall(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    group_data = await rq.get_group(int(callback.data.split('_')[1]))
    await serv.send_note_from_db(callback, group_data.notes_ls)
    await state.clear()


# The handler deletes the group by id from the callback, sends a deletion message
# and clears the FSM state.
@router.callback_query(StateFilter(GroupStates.select_group_to_view), F.data.startswith(CallbackPrefix.DEL))
async def process_del_group(callback: CallbackQuery, state: FSMContext):
    try:
        await rq.del_group(int(callback.data.split('_')[1]))
        await callback.message.edit_text(LEXICON_MESSAGES['group_deleted'])
        await state.clear()
    except:
        await callback.message.edit_text(LEXICON_ERRORS['error_group_deleting'])


