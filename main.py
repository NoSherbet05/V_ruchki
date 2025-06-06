import telebot
from telebot import types
import csv

bot = telebot.TeleBot('8037360232:AAG5BjdTU-357eNZu94BnbCWRA866xrU6jg')
reader_counter = 1
favorites = {}
favorites_counter = {}


@bot.callback_query_handler(func=lambda callback: True)
def callback_message_menu(callback):
    global reader_counter, favorites, favorites_counter
    chat_id = callback.message.chat.id

    if callback.data == 'cont':
        btn1 = types.InlineKeyboardButton("❔ FAQ", callback_data='inf')
        btn2 = types.InlineKeyboardButton("Просмотр карточек 🐕", callback_data='browse')
        btn3 = types.InlineKeyboardButton("Избранное ️️️❤️", callback_data='favorites')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn1, btn2)
        markup.row(btn3)

        bot.delete_message(chat_id, callback.message.message_id)
        try:
            bot.delete_message(chat_id, callback.message.message_id - 1)
        except Exception as e:
            print(f"Error deleting message: {e}")
        img = "start_img.jpg"
        with open(img, 'rb') as photo:
            bot.send_photo(callback.message.chat.id, photo, caption='*Что вас интересует сейчас?*', reply_markup=markup,
                           parse_mode='Markdown')

    elif callback.data == 'inf':
        btn_link = types.InlineKeyboardButton("🔗 Ссылка на канал", url='https://t.me/vruchke')
        btn_back = types.InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn_back)
        markup.row(btn_link)

        bot.delete_message(chat_id, callback.message.message_id)
        bot.send_message(chat_id, '⚡ <b>Что вы найдёте у нас?</b>\n\n'
                                  '🔥 <b>Карточки с собаньками:</b> небольшие информационные слайды, которые можно «свайпать» и подбирать собаку, подходящую под все необходимые параметры\n\n '
                                  '🔥 <b>Раздел с полезными материалами:</b> большое количество подкастов, статей и курсов от наших специалистов\n\n'
                                  '🔥 <b>Последние новости и анонсы разных мероприятий:</b> в нашем приложении Вы всегда будете знать, кто же стал счастливчиком и отправился на мягкий диван, а также всегда сможете поучаствовать в наших активностях, которых будет очень много.\n\n'
                                  '<b>Но это еще далеко не все, поэтому подпишитесь на канал, чтобы не пропустить ничего важного, и пригласите друзей — вместе мы сможем помочь большему количеству животных!</b>',
                         reply_markup=markup, parse_mode='html')

    elif callback.data == 'browse':
        bot.delete_message(chat_id, callback.message.message_id)
        browse(callback.message)

    elif callback.data == 'next':
        if reader_counter + 1 < 6:
            reader_counter += 1
            browse(callback.message)
            bot.delete_message(chat_id, callback.message.message_id)
        else:
            bot.answer_callback_query(callback.id, 'На этом пока все!')

    elif callback.data == 'like':
        if chat_id not in favorites:
            favorites[chat_id] = []
        if reader_counter - 1 not in favorites[chat_id]:
            favorites[chat_id].append(reader_counter - 1)
            bot.answer_callback_query(callback.id, "Карточка добавлена в избранное!")
        else:
            bot.answer_callback_query(callback.id, "Карточка уже в избранном!")

    elif callback.data == 'more_favorite':
        favorite_index = favorites[chat_id][favorites_counter[chat_id]]
        with open('DataSet.csv', 'r', encoding='cp1251') as file:
            rows = list(csv.reader(file))[1:]
            row = rows[favorite_index]
            sex = row[1]
            age = row[2]
            location = row[3]
            link = row[4]

        btn_back = types.InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')
        btn_link = types.InlineKeyboardButton("🔗 Контакты", url='https://vk.com/vruchke')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn_back)
        markup.row(btn_link)
        bot.send_message(
            chat_id,
            f'<b>Пол:</b> {sex}\n\n'
            f'<b>Возраст:</b> {age}\n\n'
            f'<b>Адрес приюта:</b> {location}\n\n'
            f'<b>Мед. карта:</b> {link}\n\n',
            reply_markup=markup, parse_mode='html')

    elif callback.data == 'favorites':
        bot.delete_message(chat_id, callback.message.message_id)
        show_favorites(callback.message)

    elif callback.data == 'next_favorite':
        try:
            bot.delete_message(chat_id, callback.message.message_id - 1)
        except Exception as e:
            print(f"Error deleting message: {e}")
        bot.delete_message(chat_id, callback.message.message_id)
        show_favorites(callback.message, next_card=True)

    elif callback.data == 'back_to_menu':
        btn1 = types.InlineKeyboardButton("❔ FAQ", callback_data='inf')
        btn2 = types.InlineKeyboardButton("Просмотр карточек 🐕", callback_data='browse')
        btn3 = types.InlineKeyboardButton("Избранное ️️️❤️", callback_data='favorites')

        markup = types.InlineKeyboardMarkup()
        markup.row(btn1, btn2)
        markup.row(btn3)

        try:
            bot.delete_message(chat_id, callback.message.message_id - 1)
        except Exception as e:
            print(f"Error deleting message: {e}")
        bot.delete_message(chat_id, callback.message.message_id)
        reader_counter = 1

        img = "start_img.jpg"
        with open(img, 'rb') as photo:
            bot.send_photo(callback.message.chat.id, photo, caption='''*Добро пожаловать в бота "В Ручки"*!''',
                           reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['start'])
def start(message):
    btn_cont = types.InlineKeyboardButton("Дальше ➡️", callback_data='cont')
    markup = types.InlineKeyboardMarkup()
    markup.row(btn_cont)
    img = "start_img.jpg"
    with open(img, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption='''*Добро пожаловать в бота "В Ручки"*!''', reply_markup=markup,
                       parse_mode='Markdown')


@bot.message_handler(commands=['show_favorites'])
def show_favorites(message, next_card=False):
    global favorites, favorites_counter
    chat_id = message.chat.id
    if chat_id not in favorites or not favorites[chat_id]:
        btn_back = types.InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn_back)
        bot.send_message(chat_id, "Ваш список избранного пуст.", reply_markup=markup)
        return

    if chat_id not in favorites_counter:
        favorites_counter[chat_id] = 0
    if next_card:
        favorites_counter[chat_id] = (favorites_counter[chat_id] + 1) % len(favorites[chat_id])

    favorite_index = favorites[chat_id][favorites_counter[chat_id]]
    with open('DataSet.csv', 'r', encoding='cp1251') as file:
        rows = list(csv.reader(file))[1:]
        row = rows[favorite_index]

    name = row[0]
    img = row[5]

    btn_next = types.InlineKeyboardButton("Следующая ➡️", callback_data='next_favorite')
    btn_more = types.InlineKeyboardButton("ℹ️ Развернуть", callback_data='more_favorite')
    btn_back = types.InlineKeyboardButton("Покинуть избранное", callback_data='back_to_menu')
    markup = types.InlineKeyboardMarkup()
    markup.row(btn_more, btn_next)
    markup.row(btn_back)

    with open(img, 'rb') as photo:
        bot.send_photo(chat_id, photo, caption=f'*{name}* 🐶', reply_markup=markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda callback: callback.data == 'more_favorite')
def more_favorite(callback):
    global favorites, favorites_counter
    chat_id = callback.message.chat.id
    with open('DataSet.csv', 'r', encoding='cp1251') as file:
        row = list(csv.reader(file))[reader_counter]

    sex = row[1]
    age = row[2]
    location = row[3]
    link = row[4]
    btn_back = types.InlineKeyboardButton("Назад", callback_data='back_to_menu')
    btn_link = types.InlineKeyboardButton("🔗 Контакты", url='https://vk.com/vruchke')
    markup = types.InlineKeyboardMarkup()
    markup.row(btn_back)
    markup.row(btn_link)

    bot.delete_message(chat_id, callback.message.message_id)
    bot.send_message(
        chat_id,
        f'<b>Пол:</b> {sex}\n\n'
        f'<b>Возраст:</b> {age}\n\n'
        f'<b>Адрес приюта:</b> {location}\n\n'
        f'<b>Мед. карта:</b> {link}\n\n',
        reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=['browse'])
@bot.callback_query_handler(func=lambda callback: callback.data == 'browse')
def browse(message):
    global reader_counter
    with open('DataSet.csv', 'r', encoding='cp1251') as file:
        row = list(csv.reader(file))[reader_counter]
        name = row[0]
        img = row[5]

        btn_back = types.InlineKeyboardButton("⬅️ В меню", callback_data='back_to_menu')
        btn_next = types.InlineKeyboardButton("Продолжить ➡️", callback_data='next', parse_mode='Markdown')
        btn_like = types.InlineKeyboardButton("❤️", callback_data='like')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn_back, btn_next)
        markup.row(btn_like)

        with open(img, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=f'*{name}* 🐶', reply_markup=markup, parse_mode='Markdown')


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
