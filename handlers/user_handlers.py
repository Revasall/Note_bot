from copy import deepcopy
import asyncio


from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo, InputMediaDocument
from database.database import user_dict_template, note_template, users_db
from database.methods import send_note_from_db
import database.requests as rq

from filters.filters import IsDelNoteCallbackData, IsEditNoteCallbackData
from keyboards.keyboards_builder import (static_keyboard,
                                         list_of_notes_keyboard,
                                         list_of_group_keyboard,
                                         creating_a_note_keyboard,
                                         select_notes_for_group_keyboard,
                                         note_keyboard,
                                         cansel_keyboard,
                                         editing_a_note_keyboard,
                                         group_keyboard,
                                         delete_notes_keyboard)



from lexicon.lexicon_ru import LEXICON, LEXICON_BUTTONS


#router initialization
router = Router()

# Create a class inheriting from StatesGroup for the state group of FSM
class FSMFillForm(StatesGroup):
    fill_title_note = State()
    fill_text_note = State()
    select_add = State()
    send_image = State()
    send_video = State()
    send_doc = State()
    attach_note = State()
    fill_title_group = State()
    chose_notes_for_group = State()
    chose_note = State()
    chose_group_notes = State()
    edit_note = State()
    add_note_to_group = State()
    select_group = State()
    edit_group = State()

# ___________
# Start commands handlers
# ___________

#handler for the /start command and adding a user to the database
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text], 
                         reply_markup=static_keyboard())
    await rq.set_user(message.from_user.id)

@router.message(Command(commands='help'), StateFilter(default_state))
@router.message(F.text == LEXICON_BUTTONS['help'], StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])

@router.message(Command(commands='cansel'), ~StateFilter(default_state))
async def process_cansel_command(message: Message, state: FSMContext):
    await message.answer(LEXICON['/cansel'])
    await state.clear()

@router.callback_query(F.data == 'cansel', ~StateFilter(default_state))
async def process_cansel_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['/cansel'])
    await state.clear()



# ___________
# Create notes handlers
# ___________


@router.message(Command(commands='create_note'), StateFilter(default_state))
@router.message(F.text == LEXICON_BUTTONS['create_note'], StateFilter(default_state))
async def process_create_note_command(message: Message, state: FSMContext):
    await message.answer(LEXICON['/create_note'])
    # Set the note title state
    await state.set_state(FSMFillForm.fill_title_note)

@router.message(StateFilter(FSMFillForm.fill_title_note), F.text)
async def process_title_note_sent(message: Message, state: FSMContext):
    if len(message.text) <= 200:
        await state.update_data(title_note = message.text)
        await message.answer(LEXICON['send_text'])
        # Set the note text state
        await state.set_state(FSMFillForm.fill_text_note)
    else: 
        await message.answer(LEXICON['too_long_text'])

@router.message(StateFilter(FSMFillForm.fill_title_note))
async def warning_title(message: Message):
    await message.answer(LEXICON['warning_title'])

@router.message(StateFilter(FSMFillForm.fill_text_note), F.text)
async def process_text_note_sent(message: Message, state: FSMContext):
    note = await state.get_data()
    note['text'] = note.get('text', []) + [message.text]
    await state.set_data(note)
    await message.answer(
        text=LEXICON['data_saved'],
        reply_markup=creating_a_note_keyboard()
        )
    await state.set_state(FSMFillForm.select_add)

#Select_add_data_for_note

#Text
@router.callback_query(StateFilter(FSMFillForm.select_add), F.data == 'add_text')
async def process_add_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON['message_add_text'],
        reply_markup=cansel_keyboard())
    await state.set_state(FSMFillForm.fill_text_note)

#image
@router.callback_query(StateFilter(FSMFillForm.select_add), F.data == 'add_image')
async def start_add_image(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON['message_add_image'],
        reply_markup=cansel_keyboard())
    await state.set_state(FSMFillForm.send_image)
    
    
@router.message(StateFilter(FSMFillForm.send_image), F.photo)
async def send_image_for_note(message: Message, state: FSMContext):
    note = await state.get_data()
    note['images'] = note.get('images', []) + [message.photo[-1].file_id]
    await state.set_data(note)
    await message.answer(
        text=LEXICON['data_saved'],
        reply_markup=creating_a_note_keyboard()
        )
    await state.set_state(FSMFillForm.select_add)

@router.message(StateFilter(FSMFillForm.send_image))
async def warning_image(message: Message):
    await message.answer(
        text=LEXICON['warning_image'],
        reply_markup=cansel_keyboard())

#Video
@router.callback_query(StateFilter(FSMFillForm.select_add), F.data == 'add_video')
async def start_add_video(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON['message_add_video'],
        reply_markup=cansel_keyboard())
    await state.set_state(FSMFillForm.send_video)

@router.message(StateFilter(FSMFillForm.send_video), F.video)
async def send_video_for_note(message: Message, state: FSMContext):
    note = await state.get_data()
    note['video'] = note.get('video', []) + [message.video.file_id]
    await state.set_data(note)
    await message.answer(
        text=LEXICON['data_saved'],
        reply_markup=creating_a_note_keyboard()
        )
    await state.set_state(FSMFillForm.select_add)

@router.message(StateFilter(FSMFillForm.send_video))
async def warning_video(message: Message):
    await message.answer(
        text=LEXICON['warning_video'],
        reply_markup=cansel_keyboard())

#Doc
@router.callback_query(StateFilter(FSMFillForm.select_add), F.data == 'add_doc')
async def start_add_doc(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON['message_add_doc'],
        reply_markup=cansel_keyboard())
    await state.set_state(FSMFillForm.send_doc)

@router.message(StateFilter(FSMFillForm.send_doc), F.document)
async def send_doc_for_note(message: Message, state: FSMContext):
    note = await state.get_data()
    note['doc'] = note.get('doc', []) + [message.document.file_id]
    await state.set_data(note)
    await message.answer(
        text=LEXICON['data_saved'],
        reply_markup=creating_a_note_keyboard()
        )
    await state.set_state(FSMFillForm.select_add)

@router.message(StateFilter(FSMFillForm.send_doc))
async def warning_doc(message: Message):
    await message.answer(
        text=LEXICON['warning_doc'],
        reply_markup=cansel_keyboard())

#Link to note

#Complete creating
@router.callback_query(StateFilter(FSMFillForm.select_add), F.data == 'complete_creating')
async def process_complete_creating(callback: CallbackQuery, state: FSMContext):
    note = await state.get_data()
    # users_db[callback.from_user.id]['groups']['1::all_notes'][note['title_note']] = note
    await rq.set_note(note, callback.from_user.id)
    await state.clear()
    await callback.message.edit_text(
        LEXICON['completing_note_creating']
        )





# ___________
# Create group handlers
# ___________



@router.message(Command(commands='create_group'), StateFilter(default_state))
@router.message(F.text == LEXICON_BUTTONS['create_group'], StateFilter(default_state))
async def process_create_group_command(message: Message, state: FSMContext):
    await message.answer(LEXICON[message.text])
    await state.set_state(FSMFillForm.fill_title_group)

@router.message(StateFilter(FSMFillForm.fill_title_group), F.text)
async def input_title_for_group(message: Message, state: FSMContext):
    if len(message.text) <= 200:
        note_list = await rq.get_note_titles(message.from_user.id)
        await state.update_data(title_group_note=message.text)
        await message.answer(
            text=LEXICON['select_notes_for_group'],
            reply_markup=select_notes_for_group_keyboard(note_list)
        )
        await state.set_state(FSMFillForm.chose_group_notes)
    else: 
        await message.answer(LEXICON['too_long_text'])

@router.callback_query(F.data.startswith('select_'), StateFilter(FSMFillForm.chose_group_notes))
async def process_note_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    note_list = await rq.get_note_titles(callback.from_user.id)
    group = await state.get_data()
    group['select_notes'] = group.get('select_notes', []) + [int(callback.data.split('_')[1])]
    await callback.message.edit_reply_markup(
        reply_markup=select_notes_for_group_keyboard(
            note_list,
            group['select_notes'])
            )
    await state.set_data(group)

@router.callback_query(F.data.startswith('del_'), StateFilter(FSMFillForm.chose_group_notes))
async def process_note_delete_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    note_list = await rq.get_note_titles(callback.from_user.id)
    group = await state.get_data()
    
    try:
        group['select_notes'].remove(int(callback.data.split('_')[1]))
        await callback.message.edit_reply_markup(
        reply_markup=select_notes_for_group_keyboard(
            note_list,
            group['select_notes'])
            )
    except: 
        callback.answer(
            text=LEXICON['warning_del_note'], 
            show_alert=True)

    await state.set_data(group)

@router.callback_query(F.data == 'finish_selection', StateFilter(FSMFillForm.chose_group_notes))
async def process_finish_selection(callback: CallbackQuery, state: FSMContext):
    group = await state.get_data()
    try:
        if 'select_notes' in group:  
            if group['select_notes']:
                await callback.message.edit_text(
                    LEXICON['finish_selection_text'])
                await rq.set_group(group['title_group_note'], group['select_notes'], callback.from_user.id)
                await state.clear()
            else:
                await callback.answer(text=LEXICON['no_select_note'])
        else:
            await callback.answer(text=LEXICON['no_select_note'])
    except:
        await callback.answer(text=LEXICON['warning_finish_selection'])
    







# ___________
# Select note handlers
# ___________



@router.message(Command(commands='select_note'), StateFilter(default_state))
@router.message(F.text == LEXICON_BUTTONS['select_note'], StateFilter(default_state))
async def process_select_group_command(message: Message, state: FSMContext):
    groups = await rq.get_group_titles(message.from_user.id)
    if groups:
        await message.answer(
            text=LEXICON['/select_group'],
            reply_markup=list_of_group_keyboard(groups)
            )
        await state.set_state(FSMFillForm.chose_note)
        
    else:
        notes = await rq.get_note_titles(message.from_user.id)
        await message.answer(
            text=LEXICON['/select_note'],
            reply_markup=list_of_notes_keyboard(notes))
        await state.set_state(FSMFillForm.chose_note)

@router.callback_query(F.data=='all_notes', StateFilter(FSMFillForm.chose_note))
async def process_select_note_command(callback: CallbackQuery, state: FSMContext):
    notes = await rq.get_note_titles(callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON['/select_note'],
        reply_markup=list_of_notes_keyboard(notes))
    await state.set_state(FSMFillForm.chose_note)

@router.callback_query(F.data.startswith('group_'), StateFilter(FSMFillForm.chose_note))
async def process_select_note_command(callback: CallbackQuery, state: FSMContext):
    group = await rq.get_group(int(callback.data.split('_')[1]))
    for row in group:
        group_data = row[0]

    group_notes = await rq.get_note_titles(callback.from_user.id, group_data.notes_ls)
    if group_notes:
        await callback.message.edit_text(
            text=LEXICON['/select_note'],
            reply_markup=list_of_notes_keyboard(group_notes)
            )
    else: 
        await callback.message.answer(text=LEXICON['not_notes_in_group'], )
    
@router.callback_query(F.data == 'cansel', StateFilter(FSMFillForm.chose_note))
async def process_cansel_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    

@router.callback_query(F.data.startswith('note_'), StateFilter(FSMFillForm.chose_note))
async def process_get_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await send_note_from_db(callback, [int(callback.data.split('_')[1])])
    await callback.message.answer(
        text=LEXICON['note_menu'],
        reply_markup=note_keyboard(callback.data.split('_')[1])
    )

    await state.clear()








# Edit note handlers

@router.callback_query(F.data.endswith('_edit'), StateFilter(default_state))
async def process_edit_note(callback: CallbackQuery, state: FSMContext):
    note_id = int(callback.data.split('_')[0])
    # for row in note:
    #     note_data = row[0]
    await state.set_state(FSMFillForm.edit_note)
    await state.update_data(note_id=note_id)
    await callback.message.edit_text(
        text=LEXICON['input_edit_message'],
        reply_markup=cansel_keyboard())


@router.message(StateFilter(FSMFillForm.edit_note))
async def process_edit_note_sent(message: Message, state: FSMContext):
    note_data = await state.get_data()
    note_data['text'] = note_data.get('text', []) + [message.text]
    await state.set_data(note_data)
    await message.answer(
        text=LEXICON['data_saved'],
        reply_markup=editing_a_note_keyboard()
        )
    
    
#add text
@router.callback_query(StateFilter(FSMFillForm.edit_note), F.data == 'add_text')
async def process_add_edit_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON['message_add_text'],
        reply_markup=cansel_keyboard())

#Complete editing
@router.callback_query(StateFilter(FSMFillForm.edit_note), F.data == 'complete_editing')
async def process_complete_editing(callback: CallbackQuery, state: FSMContext):
    note_data = await state.get_data()
    await rq.edit_note(note_data['note_id'], note_data['text'])
    await callback.message.edit_text(LEXICON['completing_note_editing'])
    await state.clear()


# Delete note handlers

@router.callback_query(F.data.endswith('_del'), StateFilter(default_state))
async def del_note(callback: CallbackQuery, state: FSMContext):
    note_id = int(callback.data.split('_')[0])
    try:
        await rq.del_note(note_id)
    # for group in users_db[callback.from_user.id]['groups'].keys():
    #     if group == '1::all_notes':
    #         del users_db[callback.from_user.id]['groups'][group][note]
    #     else:
    #         if note in users_db[callback.from_user.id]['groups'][group]: 
    #             users_db[callback.from_user.id]['groups'][group].remove(note)
        await callback.message.edit_text(LEXICON['completing_note_deleting'])
    except:
        await callback.message.edit_text(LEXICON['warning_note_deleting'])

# Add to group 
@router.callback_query(F.data.endswith('_add_g'), StateFilter(default_state))
# async def button_add_to_group(callback: CallbackQuery, state: FSMContext):
#     if len(users_db[callback.from_user.id]['groups'].keys()) > 1:
#         note = search_note(callback.from_user.id, callback.data[:-6])
#         await state.set_state(FSMFillForm.add_note_to_group)
#         await callback.message.edit_text(
#             LEXICON['select_group_for_note'],
#             reply_markup=list_of_group_keyboard(*list(users_db[callback.from_user.id]['groups'].keys())[1:]))
#         await state.update_data(note_name = note)
#     else:
#         await callback.answer(LEXICON['no_groups'], show_alert=True)

@router.callback_query(F.data.endswith('_select_g'), StateFilter(FSMFillForm.add_note_to_group))
async def process_add_to_group(callback: CallbackQuery, state: FSMContext):
    note = await state.get_data()
    group = search_group(callback.from_user.id, callback.data[:-9])
    if note['note_name'] not in users_db[callback.from_user.id]['groups'][group]:
        users_db[callback.from_user.id]['groups'][group].append(note['note_name'])
        await callback.message.edit_text(LEXICON['finish_add_note'])
        await state.clear()   
    else:
        await callback.answer(LEXICON['warning_add_note_to_group'], show_alert=True)

# Hide keyboard
@router.callback_query(F.data == 'hide', StateFilter(default_state))
async def process_cansel_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()


# ___________
# Select group handlers
# ___________



@router.message(Command(commands='select_group'), StateFilter(default_state))
async def process_select_group(message: Message, state: FSMContext):
    groups = await rq.get_group_titles(message.from_user.id)
    if groups:
        await message.answer(
            text=LEXICON['/select_group'],
            reply_markup=list_of_group_keyboard(groups)
            )
        await state.set_state(FSMFillForm.select_group)
    else:
        await message.answer(LEXICON['no_notes'])

@router.callback_query(F.data.startswith('group_'), StateFilter(FSMFillForm.select_group))
async def process_get_group(callback: CallbackQuery, state: FSMContext):
    group = await rq.get_group(int(callback.data.split('_')[1]))
    for row in group:
        group_data = row[0]
    await callback.message.edit_text(
        text=group_data.title,
        reply_markup=(group_keyboard(int(callback.data.split('_')[1])))
        )
    # await state.update_data(title_group_note=group,notes=notes_gr )


#Edit list of notes
@router.callback_query(F.data.startswith('edit_'), StateFilter(FSMFillForm.select_group))
async def process_edit_list_of_notes(callback: CallbackQuery, state: FSMContext):
    group = await rq.get_group(int(callback.data.split('_')[1]))
    for row in group:
        group_data = row[0]
    notes = await rq.get_note_titles(callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON['select_notes_for_group'],
        reply_markup=
        select_notes_for_group_keyboard(notes, group_data.notes_ls)
        )
    
    await state.update_data(select_notes=group_data.notes_ls)
    await state.set_state(FSMFillForm.chose_group_notes)

#Notes_wall
@router.callback_query(F.data.startswith('wall_'), StateFilter(FSMFillForm.select_group))
async def notes_wall(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    group = await rq.get_group(int(callback.data.split('_')[1]))
    for row in group:
        group_data = row[0]

    await send_note_from_db(callback, group_data.notes_ls)
    await state.clear()

@router.callback_query(F.data.startswith('del_'), StateFilter(FSMFillForm.select_group))
async def del_note(callback: CallbackQuery, state: FSMContext):
    await rq.del_group(int(callback.data.split('_')[1]))
    await callback.message.edit_text(LEXICON['group_is_deleted'])
    await state.clear()

