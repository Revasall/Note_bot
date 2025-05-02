from sqlalchemy import BigInteger, String, Text, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='postgresql+asyncpg://postgres:123zxc456vbn@localhost:5432/notes_bot')

async_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]       #Название
    text = mapped_column(ARRAY(Text))         #Текст заметок списком
    images = mapped_column(ARRAY(String))     #Id заметок списком 
    video = mapped_column(ARRAY(String))        #Id видео списком 
    files= mapped_column(ARRAY(String))        #Id файлов списком
    user_id = mapped_column(Integer, ForeignKey('users.id'))

class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    notes_ls= mapped_column(ARRAY(Integer))  
    user_id = mapped_column(Integer, ForeignKey('users.id'))

async def async_models_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)