import telebot
from dotenv import load_dotenv, find_dotenv
import os
from telebot import types
from pprint import pprint



import haiku_maker
import image_generator
import sql_handler
import title_maker

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.environ.get('TOKEN'))
makeH = haiku_maker.HaikuM()
makeT = title_maker.Title()


@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(chat_id=msg.chat.id, text=f'Привет {msg.from_user.first_name}!')
    choise(msg)

def choise(msg):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Создать новое хайку', callback_data='create')
    btn2 = types.InlineKeyboardButton('Прочитать уже созданное хайку', callback_data='read')
    btn3 = types.InlineKeyboardButton('Ничего не делать', callback_data='nothing')
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    bot.send_message(chat_id=msg.chat.id, text='Что будем делать?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('create'))
def create_haiku(call):
    sql = sql_handler.SQLhandler()
    msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Пожалуйста подождите.")
    haiku_text = makeH.make_haiku()
    image, path = image_generator.make_image(haiku_text)
    title = makeT.make_title()
    read_haiku = f'{haiku_text}\n{title[0]} {title[1]}'
    bot.delete_message(chat_id=call.message.chat.id, message_id=msg.message_id)
    bot.send_photo(chat_id=call.message.chat.id, photo=image, caption=read_haiku)
    sql.dump_haiku(f'{title[0]} {title[1]}', haiku_text, path)
    choise(msg)

@bot.callback_query_handler(func=lambda call: call.data.startswith('read'))
def read_haiku(call):
    sql = sql_handler.SQLhandler()
    title, haiku_text, image_path = sql.get_haiku()
    bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
    random_haiku = f'{haiku_text}{title}'
    with open(image_path, 'rb') as image:
        msg = bot.send_photo(chat_id=call.message.chat.id, photo=image, caption=random_haiku)
    choise(msg)

@bot.callback_query_handler(func=lambda call: call.data.startswith('nothing'))
def nothing(call):
    bot.edit_message_text(text=f'{call.from_user.first_name} для возобновления работы просто пропишите команду: \n/start@HaikuCreate_bot',
                          chat_id=call.message.chat.id,message_id=call.message.id)

bot.infinity_polling()


