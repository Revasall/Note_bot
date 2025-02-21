from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON, LEXICON_BUTTONS

def static_keyboard():
    button_create_note = KeyboardButton(text='/create_note')
    button_chose_note = KeyboardButton(text='/chose_note')
    button_other =KeyboardButton(text=LEXICON_BUTTONS['other'])

    return ReplyKeyboardMarkup(
        keyboard=[[button_create_note, button_chose_note], [button_other]],
        resize_keyboard=True,
        one_time_keyboard=True)

def list_of_group_keyboard(*args: str) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    for button in args:
        if button == 'all_notes':
            kb_builder.row(InlineKeyboardButton(
                text=LEXICON_BUTTONS['all_notes'],
                callback_data=f'{button}_select_g',
        ))
        else: 
            kb_builder.row(InlineKeyboardButton(
                text=button,
                callback_data=f'{button}_select_g',
        ))
    # Add button "Cancel" to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cansel'],
            callback_data='cansel'
        )
    )
    
    return kb_builder.as_markup()

def list_of_note_keyboard(*args: str) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    for button in args:
        kb_builder.row(InlineKeyboardButton(
            text=button,
            callback_data=f'{button}_select_n',
        ))
    # Add button "Cancel" to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cansel'],
            callback_data='cansel'
        )
    )
    
    return kb_builder.as_markup()

def creating_a_note_keyboard() -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_text'],
            callback_data='add_text' 
            ),
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_image'],
            callback_data='add_image'
            ),
        width=2
    )
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_video'],
            callback_data='add_video'
            ),
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_doc'],
            callback_data='add_doc'
            ),
        width=2
    )
    # Add "Cancel" button to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['complete_creating'],
            callback_data='complete_creating'
        )
    )
    return kb_builder.as_markup()

def note_keyboard(note_key) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit'],
            callback_data=f'{note_key}_edit' 
            ),
        InlineKeyboardButton(
            text=LEXICON['del'],
            callback_data=f'{note_key}_del'
            ),
        width=2
    )

    # Add "Cancel" button to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['hide'],
            callback_data='hide'
        )
    )
    return kb_builder.as_markup()

def cansel_keyboard() -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    kb_builder.row(
        InlineKeyboardButton(
            text=f'{LEXICON['cansel']}',
            callback_data='cansel' 
            )
    )

    return kb_builder.as_markup()

def delete_notes_keyboard(*args: str) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    for button in args:
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{LEXICON['del']} {button}',
                callback_data=f'{button}bot_del'
            )
        )
    # Add "Cancel" button to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cansel'],
            callback_data='cansel'
        )
    )
    return kb_builder.as_markup()

def chose_notes_for_group_keyboard(*args: str, chose_note: list[str] = []):
        # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    for button in args:
        if button in chose_note:
            kb_builder.row(InlineKeyboardButton(
                text=f'✅ {button}',
                callback_data=f'{button}_del_sel_g',
            ))
        else: 
            kb_builder.row(InlineKeyboardButton(
                text=button,
                callback_data=F'{button}_select_g',
            ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['finish selection'],
            callback_data='finish_selection'
        )
    )       
    # Add button "Cancel" to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cansel'],
            callback_data='cansel'
        )
    )

    return kb_builder.as_markup()