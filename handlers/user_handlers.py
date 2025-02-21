from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo, InputMediaDocument
from database.database import user_dict_template, note_template, users_db

from filters.filters import IsDelNoteCallbackData, IsEditNoteCallbackData
from keyboards.keyboards_builder import (static_keyboard,
                                         list_of_note_keyboard,
                                         list_of_group_keyboard,
                                         creating_a_note_keyboard,
                                         chose_notes_for_group_keyboard,
                                         note_keyboard,
                                         cansel_keyboard,
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

# ___________
# Start commands handlers
# ___________

#handler for the /start command and adding a user to the database
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text], 
                         reply_markup=static_keyboard())
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])

@router.message(Command(commands='cansel'), ~StateFilter(default_state))
async def process_cansel_command(message: Message, state: FSMContext):
    await message.answer(LEXICON['/cansel'])
    await state.clear()



# ___________
# Create notes handlers
# ___________


@router.message(Command(commands='create_note'), StateFilter(default_state))
async def process_create_note_command(message: Message, state: FSMContext):
    await message.answer(LEXICON[message.text])
    # Set the note title state
    await state.set_state(FSMFillForm.fill_title_note)

@router.message(StateFilter(FSMFillForm.fill_title_note), F.text)
async def process_title_note_sent(message: Message, state: FSMContext):
    await state.update_data(title_note = message.text)
    await message.answer(LEXICON['send_text'])
    # Set the note text state
    await state.set_state(FSMFillForm.fill_text_note)

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
    users_db[callback.from_user.id]['groups']['all_notes'][note['title_note']] = note
    print(users_db)
    await state.clear()
    await callback.message.edit_text(LEXICON['completing_note_creating'])





# ___________
# Create group handlers
# ___________



@router.message(Command(commands='create_group'), StateFilter(default_state))
async def process_create_group_command(message: Message, state: FSMContext):
    await message.answer(LEXICON[message.text])
    await state.set_state(FSMFillForm.fill_title_group)

@router.message(StateFilter(FSMFillForm.fill_title_group), F.text)
async def input_title_for_group(message: Message, state: FSMContext):
    await state.update_data(title_group_note = message.text)
    await message.answer(
        text=LEXICON['chose_notes_for_group'],
        reply_markup=chose_notes_for_group_keyboard(*users_db[message.from_user.id]['groups']['all_notes'].keys())
    )
    await state.set_state(FSMFillForm.chose_group_notes)

@router.callback_query(F.data.endswith('_select_g'), StateFilter(FSMFillForm.chose_group_notes))
async def process_note_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    group = await state.get_data()
    group['notes'] = group.get('notes', []) + [callback.data[:-9]]
    await callback.message.edit_reply_markup(
        reply_markup=chose_notes_for_group_keyboard(
            *users_db[callback.from_user.id]['groups']['all_notes'].keys(),
            chose_note=group['notes'])
            )
    await state.set_data(group)

@router.callback_query(F.data.endswith('_del_sel_g'), StateFilter(FSMFillForm.chose_group_notes))
async def process_note_delete_selection(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    group = await state.get_data()
    try:
        group['notes'].remove(callback.data[:-10])
        await callback.message.edit_reply_markup(
        reply_markup=chose_notes_for_group_keyboard(
            *users_db[callback.from_user.id]['groups']['all_notes'].keys(),
            chose_note=group['notes'])
            )
    except: 
        callback.answer(
            text=LEXICON['warning_del_note'], 
            show_alert=True)

    await state.set_data(group)

@router.callback_query(F.data == 'finish_selection', StateFilter(FSMFillForm.chose_group_notes))
async def process_finish_selection(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['finish_selection_text'])
    group = await state.get_data()
    users_db[callback.from_user.id]['groups'][group['title_group_note']] = group['notes']
    await state.clear()
    print(users_db)







# ___________
# Choose note handlers
# ___________



@router.message(Command(commands='select_note'), StateFilter(default_state))
async def process_select_group_command(message: Message, state: FSMContext):
    if users_db[message.from_user.id]['groups']:
        await message.answer(
            text=LEXICON['/select_group'],
            reply_markup=list_of_group_keyboard(*users_db[message.from_user.id]['groups'].keys())
            )
        print(*users_db[message.from_user.id]['groups'].keys())
        await state.set_state(FSMFillForm.chose_note)
    else:
        await message.answer(LEXICON['no_notes'])

@router.callback_query(F.data.endswith('_select_g'), StateFilter(FSMFillForm.chose_note))
async def process_chose_note_command(callback: CallbackQuery, state: FSMContext):
    if users_db[callback.from_user.id]['groups'][callback.data[:-9]]:
        await callback.message.edit_text(
            text=LEXICON['/select_note'],
            reply_markup=list_of_note_keyboard(*users_db[callback.from_user.id]['groups'][callback.data[:-9]])
            )
    else:
        await callback.message.answer(LEXICON['no_notes'])

@router.callback_query(F.data == 'cansel', StateFilter(FSMFillForm.chose_note))
async def process_cansel_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    

@router.callback_query(F.data.endswith('_select_n'), StateFilter(FSMFillForm.chose_note))
async def process_output_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]['title_note'],
    )
    if users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]['text']:
        for text in users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]['text']:
            await callback.message.answer(text= text)

    if 'images' in users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]:
        images = users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]['images'] 
        media_ph = [InputMediaPhoto(media=file_id) for file_id in images]
        await callback.bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=media_ph)

    if 'video' in users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]:
        video = users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]['video'] 
        media_vd = [InputMediaVideo(media=file_id) for file_id in video]
        await callback.bot.send_media_group(
            chat_id=callback.message.chat.id,
            media= media_vd)

    if 'doc' in users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]:
        doc = users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-9]]['doc'] 
        media_doc = [InputMediaDocument(media=file_id) for file_id in doc]
        await callback.bot.send_media_group(
            chat_id=callback.message.chat.id, 
            media=media_doc)

    await state.clear()








# Edit note handlers

@router.callback_query(F.data.endswith('_edit'), StateFilter(default_state))
async def process_edit_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON['input_edit_message'],
        reply_markup=cansel_keyboard())
    await state.set_state(FSMFillForm.edit_note)
    await state.update_data(title_note=callback.data[:-5])

@router.message(StateFilter(FSMFillForm.edit_note))
async def process_edit_note_sent(message: Message, state: FSMContext):
    await state.update_data(text_note = message.text)
    await message.answer(LEXICON['completing_note_editing'])
    note = await state.get_data()
    users_db[message.from_user.id]['groups']['all_notes'][note['title_note']] = note['text_note']
    print(users_db[message.from_user.id]['groups']['all_notes'])
    await state.clear()


# Delete note handlers

@router.callback_query(F.data.endswith('_del'), StateFilter(default_state))
async def del_note(callback: CallbackQuery, state: FSMContext):
    del users_db[callback.from_user.id]['groups']['all_notes'][callback.data[:-4]]
    await callback.message.edit_text(LEXICON['completing_note_deleting'])
    print(users_db)

# Hide keyboard
@router.callback_query(F.data == 'hide', StateFilter(default_state))
async def process_cansel_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()






@router.message(Command(commands='notes_wall'))
async def process_notes_wall_command(message: Message):
    await message.answer(LEXICON[message.text])