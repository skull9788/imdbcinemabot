import telebot
import random
from config import TOKEN
from parser import top250_IMDB
from telebot import types
import sqlite3

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветствую! Пожалуйста, введите Ваше имя пользователя:")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    username = message.text

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users
                              (name TEXT)""")
    cursor.execute("""INSERT OR IGNORE INTO users(name) VALUES (?)""", (username,))
    connect.commit()

    kb = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Отправь', callback_data='yes')
    button_no = types.InlineKeyboardButton(text='Не хочу', callback_data='no')
    kb.add(button_yes, button_no)
    bot.send_message(message.chat.id, f'Приветствую {username}! Отправить Вам случайный фильм из топ-250 IMDB?',
                     reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True )
def callback_inline(call):
    if call.data == 'yes':
        kb_yes = types.InlineKeyboardMarkup()
        b_watch = types.InlineKeyboardButton(text='Смотрел', callback_data='watch')
        b_no_watch = types.InlineKeyboardButton(text='Интересно', callback_data='no_watch')
        b_no_thanks = types.InlineKeyboardButton(text='Не интересно', callback_data='no_thanks')
        kb_yes.add(b_watch, b_no_watch, b_no_thanks)
        random_list = random.choice(top250_IMDB)
        bot_film = '.....'.join(str(i) for i in random_list)
        bot.send_message(call.message.chat.id, bot_film, reply_markup=kb_yes)
        with open('boofer.txt', 'w', encoding='utf-8') as file:
            file.write(bot_film)
        top250_IMDB.remove(random_list)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, text='Тогда до свидания!!!')
    elif call.data == 'watch':
        kb_another = types.InlineKeyboardMarkup()
        b_another = types.InlineKeyboardButton(text='Отправить другой', callback_data='yes')
        kb_another.add(b_another)
        bot.send_message(call.message.chat.id, text='Отлично, могу отправить другой фильм!',
                         reply_markup=kb_another)
    elif call.data == 'no_watch':

        with open('boofer.txt','r') as boofer:
            film = boofer.read()
        with open('unwatched films.txt', 'a') as destination:
            destination.write(film + '\n')

        kb_another2 = types.InlineKeyboardMarkup()
        b_another2 = types.InlineKeyboardButton(text='Отправить другой', callback_data='yes')
        b_another2_1 = types.InlineKeyboardButton(text='получить файл txt', callback_data='send')
        kb_another2.add(b_another2, b_another2_1)
        bot.send_message(call.message.chat.id, text=f'Отлично, я записал, что Вы не смотрели этот фильм!',
                         reply_markup=kb_another2)
    elif call.data == 'no_thanks':
        kb_another3 = types.InlineKeyboardMarkup()
        b_another3 = types.InlineKeyboardButton(text='Отправить другой', callback_data='yes')
        kb_another3.add(b_another3)
        bot.send_message(call.message.chat.id, text='Понял, отправить другой фильм ?',
                         reply_markup=kb_another3)
    elif call.data == 'send':
        user_id = call.from_user.id
        with open('unwatched films.txt', 'rb') as txt:
            bot.send_document(chat_id=user_id, document=txt, visible_file_name='unwatched films.txt')

bot.polling(non_stop=True)



