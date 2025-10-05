"""
keyboards_builder.py — functions for creating bot keyboards.

Contains:
- keyboards for notes (list, menu, pagination)
- keyboards for groups
- universal Cancel button
"""


from aiogram.types import (KeyboardButton, 
                           ReplyKeyboardMarkup, 
                           InlineKeyboardButton, 
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_BUTTONS
from utils.utils import CallbackPrefix 

def cancel_btn() -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=LEXICON_BUTTONS['cancel'], 
        callback_data=CallbackPrefix.CANCEL
        )

def cancel_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(cancel_btn())
    return kb_builder.as_markup()


def static_keyboard():
    button_create_note = KeyboardButton(text=LEXICON_BUTTONS['create_note'])
    button_select_note = KeyboardButton(text=LEXICON_BUTTONS['select_note'])
    button_create_group = KeyboardButton(text=LEXICON_BUTTONS['create_group'])
    button_select_group = KeyboardButton(text=LEXICON_BUTTONS['select_group'])
    button_other = KeyboardButton(text=LEXICON_BUTTONS['help'])

    return ReplyKeyboardMarkup(
        keyboard=[[button_create_note, button_select_note], [button_create_group, button_select_group], [button_other]],
        resize_keyboard=True
        )

def groups_list_keyboard(group_lst: list, all_groups:bool = True) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()

    if all_groups:
        kb_builder.row(InlineKeyboardButton(
            text=LEXICON_BUTTONS['all_notes'],
            callback_data='all_notes'
            ))

    for button in group_lst:
        button_id, button_name = button
        kb_builder.row(InlineKeyboardButton(
            text=button_name, 
            callback_data=CallbackPrefix.GROUP + str(button_id)
            ))

    kb_builder.row(cancel_btn())
    
    return kb_builder.as_markup()


# The function takes a list of notes, divides them into parts, displaying a page of 10 notes and giving navigation buttons.
def notes_list_keyboard(notes_lst: list, page:int=0, page_size:int=10) -> InlineKeyboardMarkup:

    start = page * page_size
    end = start + page_size
    notes_page = notes_lst[start:end]

    kb_builder = InlineKeyboardBuilder()
    
    for button in notes_page:
        button_id, button_name = button
        kb_builder.row(InlineKeyboardButton(
            text=button_name,
            callback_data=CallbackPrefix.NOTE + str(button_id)))

    nav_btn = []
    if page > 0:
        nav_btn.append(InlineKeyboardButton(
            text='⬅️',
            callback_data=CallbackPrefix.NOTE_PAGE + str(page-1)))
    if page < (len(notes_lst)-1) // page_size:
        nav_btn.append(InlineKeyboardButton(
            text='➡️',
            callback_data=CallbackPrefix.NOTE_PAGE + str(page+1)))

    if nav_btn:
        kb_builder.row(*nav_btn)

    kb_builder.row(cancel_btn())

    return kb_builder.as_markup()

def creating_note_keyboard() -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_text'],
            callback_data='text' 
            ),
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_photo'],
            callback_data='photo'
            ),
        width=2
    )

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_video'],
            callback_data='video'
            ),
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_document'],
            callback_data='document'
            ),
        width=2
    )

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['complete_creating'],
            callback_data='complete_creating'
            ))
    
    kb_builder.row(cancel_btn())

    return kb_builder.as_markup()

def edit_note_keyboard() -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_text'],
            callback_data='add_text' 
            ),
        cancel_btn(),
        width=2
        )
    
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['complete_editing'],
            callback_data='complete_editing'
            ))

    return kb_builder.as_markup()

def note_keyboard(note_key) -> InlineKeyboardMarkup:
    
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['edit'],
            callback_data=CallbackPrefix.EDIT + str(note_key)
            ),
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['delete'],
            callback_data=CallbackPrefix.DEL + str(note_key)
            ),
        width=2
        )
    

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_to_group'],
            callback_data=CallbackPrefix.ADD + str(note_key)
            ))

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['hide'],
            callback_data='hide'
            ))
    
    return kb_builder.as_markup()

def group_keyboard(group_id: int) -> InlineKeyboardMarkup:
    
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['edit_list_notes'],
            callback_data=CallbackPrefix.EDIT + str(group_id)
            ),
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['notes_wall'],
            callback_data=CallbackPrefix.WALL + str(group_id)
            ),
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['delete'],
            callback_data=CallbackPrefix.DEL+ str(group_id)
            ),
            width=1
        )
    
    kb_builder.row(cancel_btn())

    return kb_builder.as_markup()


# If the note is already in favorites, a check mark is displayed and the button callback will be DEL, 
# which when clicked will remove it from the selected notes. 
# If the note is not in favorites, an SELECT callback is sent to add it to the list.
def select_notes_for_group_keyboard(notes: list[str], select_notes: list[str] = []):

    kb_builder = InlineKeyboardBuilder()
    
    for button in notes:
        button_id, button_name = button
        if button_id in select_notes:
            kb_builder.row(InlineKeyboardButton(
                text=f'✅ {button_name}',
                callback_data=CallbackPrefix.DEL+str(button_id),
            ))
        else: 
            kb_builder.row(InlineKeyboardButton(
                text=button_name,
                callback_data=CallbackPrefix.SELECT+str(button_id),
            ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['finish_selection'],
            callback_data='finish_selection'
        )
    )       
    
    kb_builder.row(cancel_btn())

    return kb_builder.as_markup()