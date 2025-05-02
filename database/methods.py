import database.requests as rq
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo, InputMediaDocument


async def send_note_from_db(callback: CallbackQuery, notes_ids: list[int]):
    
    for note_id in notes_ids:
        note = await rq.get_note(note_id)
        for row in note:
            note_data = row[0]

        await callback.message.answer(
            text=note_data.title
        )
        if note_data.text:
            for text in note_data.text:
                await callback.message.answer(text=text)

        if note_data.images:
            images = note_data.images
            media_ph = [InputMediaPhoto(media=file_id) for file_id in images]
            await callback.bot.send_media_group(
                chat_id=callback.message.chat.id,
                media=media_ph)

        if note_data.video:
            video = note_data.video
            media_vd = [InputMediaVideo(media=file_id) for file_id in video]
            await callback.bot.send_media_group(
                chat_id=callback.message.chat.id,
                media= media_vd)

        if note_data.files:
            doc = note_data.files
            media_doc = [InputMediaDocument(media=file_id) for file_id in doc]
            await callback.bot.send_media_group(
                chat_id=callback.message.chat.id, 
                media=media_doc)
            
