LEXICON: dict[str, str] = {
    '/start': '<b>Добрейшего дня, Мыслитель!</b>\n\nЭто бот, в котором '
              'ты можешь создавать и работать с заметками.\n\n'
              'Чтобы посмотреть список доступных '
              'команд и узнать больше о работе бота - набери /help',
    '/help': 'Как работает бот для заметок.\n\n'
             'Чтобы создать заметку, введите команду /create_note, после'
             'чего бот Вам предложит написать текст, который Вы хотите'
             'видеть в этой заметке.\n\n'
             'Чтобы объединить заметки в единую группу, введите' 
             'команду /create_group после чего выберите название для'
             'заметки и выберите все те существующие заметки, которые'
             'должны в ней находиться.\n\n'
             'Чтобы открыть существующую заметку, введите команду '
             '/chose_note и выберете необходимую заметку. После вывода'
             'бот предложит Вам её редактировать.\n\n'
             'Если Вы хотите просмотреть все заметки сразу, то введите'
             'команду /notes_wall, которая отправит Вам все существующие'
             'заметки или заметки определённой группы в случайном или'
             'существующем порядке.'
             ,
    '/create_note': 'Введите название заметки, которую Вы хотите создать',
    'warning_title': 'Название должно содержать только текст\n\n'
                     'Пожалуйста, введите корректное название\n\n', 
    'send_text': 'Спасибо, теперь введите текст заметки.',
    'warning_text': 'Заметка должна содержать только текст\n\n'
                    'Пожалуйста, корректно заполните заметку\n\n',
    'data_saved': 'Что-то ещё?',
    'completing_note_creating': 'Заметка создана и успешно добавлена в базу',
    '/create_group': 'Введите название группы для заметок, которую Вы хотите создать',
    '/chose_note': 'Выберите заметку, которую желаете открыть:',
    'edit': '🖋 Редактировать',
    'input_edit_message': 'Введите новый текст заметки:',
    'completing_note_editing': 'Заметка успешно изменена',
    'del': '🗑 Удалить',
    'completing_note_deleting': 'Заметка успешно удалена',
    'hide': 'Скрыть клавиатуру',
    'no_notes': 'Заметок не найдено',
    'message_add_text': 'Введите текст, который следует добавить',
    'message_add_image': 'Отправьте изображение, которое следует прикрепить к заметке',
    'warning_image': 'Ошибка, отправьте изображение или нажмите кнопку "отменить"',
    'message_add_video': 'Отправьте видео, которое следует прикрепить к заметке', 
    'warning_video': 'Ошибка, отправьте видео или нажмите кнопку "отменить"',
    'message_add_doc': 'Отправьте файл, которое следует прикрепить к заметке',
    'warning_doc': 'Ошибка, отправьте файл или нажмите кнопку "отменить"',
    'cansel': 'Отменить',
    '/notes_wall': 'Стена',
    '/cansel': 'Действие отменено'
}

LEXICON_BUTTONS: dict[str,str] = {
    #Static_buttons
    'create_note': 'Создать заметку',
    'chose_note': 'Выбрать заметку',
    'other': 'Другое',

    #createing a note keyboard
    'add_text': 'Текст',
    'add_image': 'Изображение',
    'add_video': 'Видео',
    'add_doc': 'Файл',
    'complete_creating': 'Завершить создание заметки'

}


LEXICON_COMMANDS = {
    '/start': 'Запустите работу бота',
    '/help': 'Помощь в работе бота',
    '/create_note': 'Создать заметку',
    '/create_group': 'Создать группу для заметок',
    '/chose_note': 'Выбрать заметку', 
    '/notes_wall': 'Создать стену из заметок',
    '/cansel': 'Отменить действие'
}
