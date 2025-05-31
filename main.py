import telebot
from telebot import types
import csv

bot = telebot.TeleBot('8037360232:AAG5BjdTU-357eNZu94BnbCWRA866xrU6jg')
reader_counter = 1


@bot.callback_query_handler(func=lambda callback: True)
def callback_message_menu(callback):
    global reader_counter
    F = open('DataSet.csv', 'r', encoding='cp1251')
    reader = list(csv.reader(F))[reader_counter]

    if callback.data == 'cont':
        btn2 = types.InlineKeyboardButton("❔ FAQ", callback_data='inf')
        btn3 = types.InlineKeyboardButton("Просмотр карточек 🐕", callback_data='browse')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn2, btn3)

        # Delete the previous messages
        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            # bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        except Exception as e:
            print(f"Error deleting message: {e}")

        bot.send_message(callback.message.chat.id, 'Что вас интересует сейчас?', reply_markup=markup, parse_mode='html')

    elif callback.data == 'inf':
        btn_link = types.InlineKeyboardButton("🔗 Ссылка на канал", callback_data='link')
        btn_back = types.InlineKeyboardButton("⬅️ Назад", callback_data='back_to_menu')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn_back)
        markup.row(btn_link)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

        bot.send_message(callback.message.chat.id, '⚡ <b>Что вы найдёте у нас?</b>\n\n'
                                                   '🔥 <b>Карточки с собаньками:</b> небольшие информационные слайды, которые можно «свайпать» и подбирать собаку, подходящую под все необходимые параметры\n\n '
                                                   '🔥 <b>Раздел с полезными материалами:</b> большое количество подкастов, статей и курсов от наших специалистов\n\n'
                                                   '🔥 <b>Последние новости и анонсы разных мероприятий:</b> в нашем приложении Вы всегда будете знать, кто же стал счастливчиком и отправился на мягкий диван, а также всегда сможете поучаствовать в наших активностях, которых будет очень много.\n\n'
                                                   '<b>Но это еще далеко не все, поэтому подпишитесь на канал, чтобы не пропустить ничего важного, и пригласите друзей — вместе мы сможем помочь большему количеству животных!</b>', reply_markup=markup, parse_mode='html')

    elif callback.data == 'browse':
        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

        browse(callback.message)


    elif callback.data == 'more':
        with open('DataSet.csv', 'r', encoding='cp1251') as file:
            reader = list(csv.reader(file))[reader_counter]
            sex = reader[1]
            age = reader[2]
            location = reader[3]
            link = reader[4]
            # breed = reader[5]
        # Порода: {}\n
        bot.send_message(callback.message.chat.id, f'<b>Пол:</b> {sex}\n\n'
                                                   f'<b>Возраст:</b> {age}\n\n'
                                                   f'<b>Адрес приюта:</b> {location}\n\n'
                                                   f'<b>Ссылка на мед. карту:</b> {link} скоро появится\n\n'
                                                   f'<b>Контакты:</b> https://vk.com/vruchke', parse_mode='html')

    elif callback.data == 'next':
        if reader_counter < len(reader):
            reader_counter += 1
        if reader_counter != len(reader):
            browse(callback.message)
        else:
            bot.send_message(callback.message.chat.id, 'На этом пока все!')
            reader_counter = 1

    elif callback.data == 'back_to_menu':
        btn2 = types.InlineKeyboardButton("❔ FAQ", callback_data='inf')
        btn3 = types.InlineKeyboardButton("Просмотр карточек 🐕", callback_data='browse')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn2, btn3)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

        bot.send_message(callback.message.chat.id, 'Что вас интересует сейчас?', reply_markup=markup)

    elif callback.data == 'link':
        bot.send_message(callback.message.chat.id, "Открыть канал: https://t.me/vruchke")

@bot.message_handler(commands=['start'])
def start(message):
    btn_cont = types.InlineKeyboardButton("Продолжить ➡️", callback_data='cont')
    markup = types.InlineKeyboardMarkup()
    markup.row(btn_cont)
    bot.send_message(message.chat.id, '''Добро пожаловать в бота "В Ручки"!''', reply_markup=markup, parse_mode='HTML')


# функция карточек
@bot.message_handler(commands=['browse'])
@bot.callback_query_handler(func=lambda callback: callback.data == 'browse')
def browse(message):
    global reader_counter
    with open('DataSet.csv', 'r', encoding='cp1251') as file:
        reader = list(csv.reader(file))[reader_counter]
        name = reader[0]
        img = reader[5]
        btn_next = types.InlineKeyboardButton("Смотреть дальше ➡️", callback_data='next', parse_mode='Markdown')
        btn_more = types.InlineKeyboardButton("ℹ️ Развернуть", callback_data='more', parse_mode='Markdown')
        markup = types.InlineKeyboardMarkup()
        markup.row(btn_more, btn_next)
        with open(img, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=f'{name} 🐶', reply_markup=markup, parse_mode='Markdown')


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)