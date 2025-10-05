import database.requests as rq
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo, InputMediaDocument


async def send_note_from_db(callback: CallbackQuery, notes_ids: list[int]):
    
    for note_id in notes_ids:
        note = await rq.get_note(note_id)

        await callback.message.answer(text=note.title)

        if note.text:
            for text in note.text:
                await callback.message.answer(text=text)

        if note.images:
            chunks = [note.images[i:i+10] for i in range(0, len(note.images), 10)]
            for chunk in chunks:
                media_ph = [InputMediaPhoto(media=file_id) for file_id in chunk]
                await callback.bot.send_media_group(chat_id=callback.message.chat.id,
                                                    media=media_ph)

        if note.video:
            media_vd = [InputMediaVideo(media=file_id) for file_id in note.video]
            await callback.bot.send_media_group(chat_id=callback.message.chat.id,
                                                media= media_vd)

        if note.files:
            media_doc = [InputMediaDocument(media=file_id) for file_id in note.files]
            await callback.bot.send_media_group(chat_id=callback.message.chat.id, 
                                                media=media_doc)
            
