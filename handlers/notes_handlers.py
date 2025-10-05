"""
notes_handlers.py - handlers for creating notes.

The chain of handlers that controls the process of creating, editing and deleting a new note:
1. The user runs the /create_note command or clicks the button.
2. The FSM goes into the awaiting_title_note state and waits for titles.
3. Having received the title, it goes to awaiting_text_note.
4. The user can add additional elements (text, photos, videos, documents).
5. When you click the "Finish" button, the note is saved in the database.
6. When the /select_note command is entered, the user enters the note selection state.
7. Selects a note group or selects the desired note from the list of all notes.
8. The note is displayed, followed by a menu: edit, add to group, or delete.
9. When the user clicks "edit," the bot enters the wait state for new data.
10. When new data is entered, the bot updates the note in the database.
11. Clicking the "Add to Group" button takes the bot to the group selection state.
12. After selecting a group, the bot updates the list of notes in the groups table within the database, adding the note.
13. Clicking "Delete" removes the note from the group.


"""

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from states.fsm_fill_form import NotesStates

from database import requests as rq
from services import services as serv
from utils.utils import CallbackPrefix
from keyboards.keyboards_builder import (creating_note_keyboard,
                                        cancel_keyboard, 
                                        groups_list_keyboard, 
                                        notes_list_keyboard, 
                                        edit_note_keyboard, 
                                        note_keyboard)

from lexicon.lexicon_ru import LEXICON_MESSAGES, LEXICON_ERRORS, LEXICON_BUTTONS


router = Router()



# --------------------
# CREATE NOTE HANDLERS
# -------------------- 

# Processes the /create_note command
# Goes to the awaiting_note_title state and waits for the user to enter a note title
@router.message(StateFilter(default_state), Command(commands='create_note'))
@router.message(StateFilter(default_state), F.text == LEXICON_BUTTONS['create_note'])
async def process_create_note_command(message: Message, state: FSMContext):
    await message.answer(LEXICON_MESSAGES['create_note'])
    await state.set_state(NotesStates.awaiting_note_title)


# Handle note title input and move to text input
@router.message(StateFilter(NotesStates.awaiting_note_title), F.text)
async def process_note_title_sent(message: Message, state: FSMContext):
    if len(message.text) <= 200:
        await state.update_data(note_title = message.text)
        await state.set_state(NotesStates.awaiting_note_text)
        await message.answer(LEXICON_MESSAGES['send_text'])
    else: 
        await message.answer(LEXICON_ERRORS['title_is_too_long']) 


# If the message type is incorrect, sends the user a warning message about the incorrect note name
@router.message(StateFilter(NotesStates.awaiting_note_title))
async def notify_invalid_title(message: Message):
    await message.answer(LEXICON_ERRORS['invalid_title']) 


# Handle note text input and move to content type selection
@router.message(StateFilter(NotesStates.awaiting_note_text), F.text)
async def process_note_text(message: Message, state: FSMContext):
    data = await state.get_data()
    data['text'] = data.get('text', []) + [message.text]
    await state.set_data(data)
    await message.answer(
                        text=LEXICON_MESSAGES['select_content'],
                        reply_markup=creating_note_keyboard() 
                        )
    await state.set_state(NotesStates.select_content_type)

# If the message type is incorrect, sends the user a warning message about the incorrect note text
@router.message(StateFilter(NotesStates.awaiting_note_text))
async def notify_invalid_text(message: Message):
    await message.answer(LEXICON_ERRORS['invalid_text']) 


# Handler handles selection of content type (text, photo, video, document) 
# in the menu for adding content to a note.
# 1) Stores the selected type in the FSM (expected_content)
# 2) Switches the state to awaiting_content
# 3) Edits the message with the tooltip text depending on the selection
@router.callback_query(StateFilter(NotesStates.select_content_type), F.data.in_(['text', 'photo', 'video', 'document'])) #!!! выправіць у клавіятуры калбэк!
async def process_select_content(callback: CallbackQuery, state: FSMContext):
    await state.update_data(expected_content=callback.data, last_message_id = callback.message.message_id)
    await state.set_state(NotesStates.awaiting_content)
    await callback.message.edit_text(
                                    text=LEXICON_MESSAGES[f'send_{callback.data}'],
                                    reply_markup=cancel_keyboard()
                                    )
    

# The handler processes the sent content depending on the expected type:
# Adds the corresponding content to state, returns the state to select_content_type
# and shows the keyboard for further actions.
@router.message(StateFilter(NotesStates.awaiting_content), F.text | F.photo | F.video |F.document)
async def process_content(message: Message, state: FSMContext):
        
    data = await state.get_data()
    expected = data.get('expected_content')

    try:
        await message.bot.delete_message(
            chat_id = message.chat.id,
            message_id = data['last_message_id'])

    except:
        None
    
    if expected == 'text' and message.text:
        data['text'] = data.get('text', []) + [message.text]
    elif expected == 'photo' and message.photo:
        data['photos'] = data.get('photos', []) + [message.photo[-1].file_id]
    elif expected == 'video' and message.video:
        data['videos'] = data.get('videos', []) + [message.video.file_id]
    elif expected == 'document' and message.document:
        data['documents'] = data.get('documents', []) + [message.document.file_id]
    
    else:
        await message.answer(
                    text=LEXICON_ERRORS['invalid_content'],
                    reply_markup=cancel_keyboard())
        return
    
    await state.set_data(data)
    await state.set_state(NotesStates.select_content_type)
    await message.answer(
                        text=LEXICON_MESSAGES['select_content'],
                        reply_markup=creating_note_keyboard()
                        )
    
@router.message(StateFilter(NotesStates.awaiting_content))
async def process_invalid_content(message: Message, state: FSMContext):
    await message.answer(
                        text=LEXICON_ERRORS['invalid_content'],
                        reply_markup=cancel_keyboard())
    

# Completing the creation of a note. 
# The handler makes a query to the database, returns the default state, 
# and sends a message about the completion of the creation.
@router.callback_query(StateFilter(NotesStates.select_content_type), F.data == 'complete_creating') #!!!complete_creation!!!
async def complete_note_creation(callback: CallbackQuery, state: FSMContext):
    note_data = await state.get_data()
    await rq.set_note(note_data, callback.from_user.id)
    await state.clear()
    await callback.message.edit_text(
        LEXICON_MESSAGES['note_created']
        )
    


# --------------------
# SELECT NOTE HANDLERS
# -------------------- 


# The process of selecting notes for viewing.
# When selecting a view, the handler checks if the user has any groups (> 1, since each user has a group "all notes")
# and sends a list of groups. If there are none, it sends a list of all notes.
@router.message(StateFilter(default_state), Command(commands='select_note'))
@router.message(StateFilter(default_state), F.text == LEXICON_BUTTONS['select_note'])
async def start_selecting_a_note(message: Message, state: FSMContext):
    groups = await rq.get_group_titles(message.from_user.id)
    if len(list(groups)) > 1:
        await message.answer(
            text=LEXICON_MESSAGES['select_group'],
            reply_markup=groups_list_keyboard(groups)
            )
        await state.set_state(NotesStates.select_note_to_view)
        
    else:
        notes = await rq.get_note_titles(message.from_user.id)
        if notes:
            await state.update_data(notes_lst = list(notes))
            await message.answer(
                text=LEXICON_MESSAGES['select_note'],
                reply_markup=notes_list_keyboard(notes))
            await state.set_state(NotesStates.select_note_to_view)
        else:
            await message.answer(text=LEXICON_MESSAGES['no_notes'])


#When selecting the "All Notes" group, the handler returns all of the user's notes.
@router.callback_query(StateFilter(NotesStates.select_note_to_view), F.data=='all_notes')
async def process_selection_note_from_all_notes(callback: CallbackQuery, state: FSMContext):
    notes = await rq.get_note_titles(callback.from_user.id)
    await state.update_data(notes_lst = list(notes))
    await callback.message.edit_text(
        text=LEXICON_MESSAGES['select_note'],
        reply_markup=notes_list_keyboard(notes))
    await state.set_state(NotesStates.select_note_to_view)


# The handler makes a request to the database to obtain the Groups object and, 
# based on the notes_id list, obtain a list of note names.
@router.callback_query(StateFilter(NotesStates.select_note_to_view), F.data.startswith(CallbackPrefix.GROUP))
async def process_selection_note_from_group(callback: CallbackQuery, state: FSMContext):
    group_data = await rq.get_group(int(callback.data.split('_')[1]))
    group_notes = await rq.get_note_titles(callback.from_user.id, group_data.notes_ls)
    await state.update_data(notes_lst = list(group_notes))
    if group_notes:
        await callback.message.edit_text(
            text=LEXICON_MESSAGES['select_note'],
            reply_markup=notes_list_keyboard(group_notes)
            )
    else: 
        await callback.message.answer(text=LEXICON_MESSAGES['no_notes_in_group'], )
        
@router.callback_query(StateFilter(NotesStates.select_note_to_view), F.data.startswith(CallbackPrefix.NOTE_PAGE))
async def process_page_navigation(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split('_')[1])
    data = await state.get_data()
    print(data)
    await callback.message.edit_reply_markup(
            reply_markup=notes_list_keyboard(data['notes_lst'], page)
            )
    

#The handler calls a method to determine and display the note data, and then attaches the note menu.
@router.callback_query(StateFilter(NotesStates.select_note_to_view), F.data.startswith(CallbackPrefix.NOTE))
async def complete_send_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await serv.send_note_from_db(callback, [int(callback.data.split('_')[1])])
    await callback.message.answer(
        text=LEXICON_MESSAGES['note_menu'],
        reply_markup=note_keyboard(callback.data.split('_')[1])
        )

    await state.clear()


#Cancel the operation and return to the default state
@router.callback_query(StateFilter(NotesStates.select_note_to_view), F.data == CallbackPrefix.CANCEL)
async def process_cancel_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()



# --------------------
# NOTE MENU HANDLERS
# -------------------- 


#The handler sends the note's ID to the cache and sets the state to pending editing.
@router.callback_query(StateFilter(default_state), F.data.startswith(CallbackPrefix.EDIT))
async def start_edit_note(callback: CallbackQuery, state: FSMContext):
    note_id = int(callback.data.split('_')[1])
    await state.set_state(NotesStates.awaiting_edit_note)
    await state.update_data(note_id=note_id)
    await callback.message.edit_text(
        text=LEXICON_MESSAGES['send_text'],
        reply_markup=cancel_keyboard())

# The рandler accepts the new text, adds it to the cache, and sends it to the keyboard for further action.
@router.message(StateFilter(NotesStates.awaiting_edit_note), F.text)
async def process_edit_note_text(message: Message, state: FSMContext):
    note_data = await state.get_data()
    note_data['text'] = note_data.get('text', []) + [message.text]
    await state.set_data(note_data)
    await message.answer(
        text=LEXICON_MESSAGES['select_content'],
        reply_markup=edit_note_keyboard()
        )
    
    
# The handler receives the callback and does not change state to wait for the next part of the new text.
@router.callback_query(StateFilter(NotesStates.awaiting_edit_note), F.data == 'add_text')
async def process_add_edit_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_MESSAGES['send_text'],
        reply_markup=cancel_keyboard())

# Finish editing the note, send new data to the database and return to the default state
@router.callback_query(StateFilter(NotesStates.awaiting_edit_note), F.data == 'complete_editing')
async def complete_edit_note(callback: CallbackQuery, state: FSMContext):
    note_data = await state.get_data()
    await rq.edit_note(note_data['note_id'], note_data['text'])
    await callback.message.edit_text(LEXICON_MESSAGES['note_edited'])
    await state.clear()


# The handler deletes a note by id from the database.
@router.callback_query(StateFilter(default_state), F.data.startswith(CallbackPrefix.DEL),)
async def process_del_note(callback: CallbackQuery, state: FSMContext):
    note_id = int(callback.data.split('_')[1])
    try:
        await rq.del_note(note_id)
        await callback.message.edit_text(LEXICON_MESSAGES['note_deleted'])
    except:
        await callback.message.edit_text(LEXICON_ERRORS['error_note_deleting']) 

# The handler saves the note IDs to the cache and displays a list of groups for selection by user ID, the callback of which will contain the group IDs.
@router.callback_query(StateFilter(default_state), F.data.startswith(CallbackPrefix.ADD))
async def button_add_to_group(callback: CallbackQuery, state: FSMContext):
    note_id = int(callback.data.split('_')[1])
    groups = await rq.get_group_titles(callback.from_user.id)
    if groups:
        await callback.message.edit_text(
            text=LEXICON_MESSAGES['select_group'],
            reply_markup=groups_list_keyboard(groups, all_groups=False))
        await state.set_state(NotesStates.select_group_for_note)
        await state.update_data(note_id=note_id)
    else:
        await callback.answer(LEXICON_MESSAGES['no_groups'], show_alert=True)

# The handler checks for the absence of a note in the selected group 
# and sends a request to the database to change the list of group notes to which the new note ID was added.
@router.callback_query(StateFilter(NotesStates.select_group_for_note), F.data.startswith(CallbackPrefix.GROUP))
async def process_add_to_group(callback: CallbackQuery, state: FSMContext):
    note_data = await state.get_data()
    group_data = await rq.get_group(int(callback.data.split('_')[1]))
    if note_data['note_id'] not in group_data.notes_ls:
        group_data.notes_ls.append(note_data['note_id'])
        await rq.update_notes_in_group(group_data.id, group_data.notes_ls)
        await callback.message.edit_text(LEXICON_MESSAGES['note_added_to_group'])
        await state.clear()   
    else:
        await callback.answer(LEXICON_ERRORS['error_adding_note'], show_alert=True) # TITLE

# Hide keyboard
@router.callback_query(StateFilter(default_state), F.data == 'hide')
async def process_cancel_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
