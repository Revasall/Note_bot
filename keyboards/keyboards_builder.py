from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON, LEXICON_BUTTONS

def static_keyboard():
    button_create_note = KeyboardButton(text=LEXICON_BUTTONS['create_note'])
    button_select_note = KeyboardButton(text=LEXICON_BUTTONS['select_note'])
    button_create_group = KeyboardButton(text=LEXICON_BUTTONS['create_group'])
    button_select_group = KeyboardButton(text=LEXICON_BUTTONS['select_group'])
    button_other =KeyboardButton(text=LEXICON_BUTTONS['help'])

    return ReplyKeyboardMarkup(
        keyboard=[[button_create_note, button_select_note], [button_create_group, button_select_group], [button_other]],
        resize_keyboard=True
        )

def list_of_group_keyboard(group_lst: list) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    kb_builder.row(InlineKeyboardButton(
                text=LEXICON_BUTTONS['all_notes'],
                callback_data='all_notes'
                )
    )
    for button in group_lst:
        button_id, button_name = button
        kb_builder.row(InlineKeyboardButton(
            text=button_name,
            callback_data=f'group_{button_id}',
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

# def list_of_notes_keyboard(*args: str) -> InlineKeyboardMarkup:
#     # Create a keyboard object
#     kb_builder = InlineKeyboardBuilder()
#     # Fill the keyboard with note buttons
#     for button in args:
#         button_id, button_name = button.split('::', maxsplit=1)
#         kb_builder.row(InlineKeyboardButton(
#             text=button_name,
#             callback_data=f'{button_id}_select_n',
#         ))
#     # Add button "Cancel" to the keyboard at the end
#     kb_builder.row(
#         InlineKeyboardButton(
#             text=LEXICON['cansel'],
#             callback_data='cansel'
#         )
#     )
    
#     return kb_builder.as_markup()

def list_of_notes_keyboard(notes_lst: list) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    for button in notes_lst:
        button_id, button_name = button
        kb_builder.row(InlineKeyboardButton(
            text=button_name,
            callback_data=f'note_{button_id}',
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
    # Add "Complete_creating" button to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['complete_creating'],
            callback_data='complete_creating'
        )
    )
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cansel'],
            callback_data='cansel'
        )
    )

    return kb_builder.as_markup()

def editing_a_note_keyboard() -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['add_text'],
            callback_data='add_text' 
            ),
        InlineKeyboardButton(
            text=LEXICON['cansel'],
            callback_data='cansel'
            ),
        width=2
    )
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTONS['complete_editing'],
            callback_data='complete_editing'
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
    #Add 'add to group' button
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['add_to_group'],
            callback_data=f'{note_key}_add_g'
        )
    )
    # Add "Cancel" button to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['hide'],
            callback_data='hide'
        )
    )
    return kb_builder.as_markup()

def group_keyboard(group_id: int) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_list_notes'],
            callback_data=f'edit_{group_id}'
            ),
        InlineKeyboardButton(
            text=LEXICON['notes_wall'],
            callback_data=f'wall_{group_id}'
            ),
        InlineKeyboardButton(
            text=LEXICON['del'],
            callback_data=f'del_{group_id}'
            ),
            width=1
    )
    # Add "Cancel" button to the keyboard at the end
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cansel'],
            callback_data='cansel'
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

def select_notes_for_group_keyboard(notes: list[str], select_notes: list[str] = []):
        # Create a keyboard object
    kb_builder = InlineKeyboardBuilder()
    # Fill the keyboard with note buttons
    for button in notes:
        button_id, button_name = button
        if button_id in select_notes:
            kb_builder.row(InlineKeyboardButton(
                text=f'✅ {button_name}',
                callback_data=f'del_{button_id}',
            ))
        else: 
            kb_builder.row(InlineKeyboardButton(
                text=button_name,
                callback_data=F'select_{button_id}',
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