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
            title=note['title_note'],
            text=note['text'],
            images = note['images'] if 'images' in note else None,
            video = note['video'] if 'video' in note else None,
            files = note['doc'] if 'doc' in note else None,
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
            print(session.execute(select(Note.id, Note.title).where(Note.id in id_list)))
            return await session.execute(select(Note.id, Note.title).where(Note.id.in_(id_list)))
        else:
            user_db_id = await session.scalar(select(User.id).where(User.tg_id==user_id))
            return await session.execute(select(Note.id, Note.title).where(Note.user_id==user_db_id))

async def get_note(note_id: int):
    async with async_session() as session: 
        return await session.execute(select(Note).where(Note.id==note_id))

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
        return await session.execute(select(Group).where(Group.id==group_id))


async def del_group(group_id:int):
    async with async_session() as session:
        await session.execute(delete(Group).where(Group.id==group_id))
        await session.commit()