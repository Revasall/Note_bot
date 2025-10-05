from database.models import async_session
from database.models import User, Note, Group
from sqlalchemy import select, update, delete
from aiogram.fsm.context import FSMContext


# Set data requests
async def set_user(tg_id: int) -> None: 
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def set_note(note, user_id: int):
    async with async_session() as session: 
        user_db_id = await session.scalar(select(User.id).where(User.tg_id==user_id))
        session.add(Note(
            title=note['note_title'],
            text=note['text'],
            images = note['photos'] if 'photos' in note else None,
            video = note['videos'] if 'video' in note else None,
            files = note['documents'] if 'documents' in note else None,
            user_id=user_db_id
            )
        )
        await session.commit()


async def set_group(title: str, notes_ls: list, user_id: int):
    async with async_session() as session:
        user_db_id = await session.scalar(select(User.id).where(User.tg_id==user_id))
        session.add(Group(
            title=title,
            notes_ls=notes_ls,
            user_id=user_db_id
            )
        )
        await session.commit()

# get note requests
async def get_note_titles(user_id:int, id_list: list = None):
    async with async_session() as session:
        if id_list:
            result = await session.execute(select(Note.id, Note.title).where(Note.id.in_(id_list)))
            return result.all()
        else:
            user_db_id = await session.scalar(select(User.id).where(User.tg_id==user_id))
            result = await session.execute(select(Note.id, Note.title).where(Note.user_id==user_db_id))
            return result.all()

async def get_note(note_id: int):
    async with async_session() as session: 
        result = await session.execute(select(Note).where(Note.id==note_id))
        return result.scalar_one_or_none()

async def edit_note(note_id:int, new_text: list):
    async with async_session() as session:
        await session.execute(update(Note).where(Note.id==note_id).values(text=new_text))
        await session.commit()

async def del_note(note_id:int):
    async with async_session() as session:
        await session.execute(delete(Note).where(Note.id==note_id))
        await session.commit()


# get group requests

async def get_group_titles(user_id:int):
    async with async_session() as session:
        user_db_id = await session.scalar(select(User.id).where(User.tg_id==user_id))
        return await session.execute(select(Group.id, Group.title).where(Group.user_id==user_db_id))

async def get_group(group_id: int):
    async with async_session() as session:
        result = await session.execute(select(Group).where(Group.id==group_id))
        return result.scalar_one_or_none()


async def del_group(group_id:int):
    async with async_session() as session:
        await session.execute(delete(Group).where(Group.id==group_id))
        await session.commit()

async def update_notes_in_group(group_id:int, new_note_list:list):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.id==group_id).values(notes_ls=new_note_list))
        await session.commit()