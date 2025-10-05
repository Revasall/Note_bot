from aiogram.fsm.state import StatesGroup, State

class NotesStates(StatesGroup):
    awaiting_note_title = State()
    awaiting_note_text = State()
    select_content_type = State()
    awaiting_content = State()
    awaiting_note_image = State()
    awaiting_note_video = State()
    awaiting_note_doc = State()
    select_note_to_view= State()
    awaiting_edit_note = State()
    select_group_for_note = State()

class GroupStates(StatesGroup):
    awaiting_group_title = State()
    select_notes_to_add = State()
    select_group_to_view = State()
    awaiting_edit_group = State()