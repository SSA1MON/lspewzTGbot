import sqlite3
import telebot.types
import func

from telebot import types, TeleBot
from config import TOKEN
from time import sleep
from datetime import datetime

bot = TeleBot(TOKEN)
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

cur_month = datetime.now().strftime("%d-%B-%Y %H:%M").split('-')[1].lower()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    """
    Функция обработчик. Обрабатывает команду /start
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("💵 Добавить приход")
    btn2 = types.KeyboardButton("🏦 Посмотреть ЗП")
    btn3 = types.KeyboardButton("🗓️ Начать новый месяц")
    markup.add(btn1, btn2, btn3)

    user_id = message.from_user.id
    func.db_table_val(month=cur_month, perv=0, garant=0, holod=0, artem=0, cleanmoney=0,
                      nonprofile=0, curbtn="None", usr_id=user_id)
    bot.send_message(message.chat.id,
                     text=f"Wassup, <b>{message.from_user.first_name}</b>!\n",
                     reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types=['text'])
def main(message: telebot.types.Message, msg: str = None) -> None:
    """
    Функция обработчик. Обрабатывает команды от кнопок в меню, при начале диалога с ботом (/start)
    """

    user_id = message.from_user.id
    if message.text == "Добавить приход" or msg == "Добавить приход":
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("Первичка", callback_data=f'pervichka|{user_id}')
        button2 = types.InlineKeyboardButton("Гарантия", callback_data=f'garant|{user_id}')
        button3 = types.InlineKeyboardButton("Холод", callback_data=f'holod|{user_id}')
        button4 = types.InlineKeyboardButton("Артём", callback_data=f'artem|{user_id}')
        button5 = types.InlineKeyboardButton("Чистые деньги", callback_data=f'cleanmoney|{user_id}')
        button6 = types.InlineKeyboardButton("Непрофиль", callback_data=f'nonprofile|{user_id}')
        markup.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(chat_id=message.chat.id, text="Выбери нужную категорию:", reply_markup=markup)

    elif message.text == "Посмотреть ЗП" or msg == "Посмотреть ЗП":
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("Январь", callback_data=f'january|{user_id}')
        button2 = types.InlineKeyboardButton("Февраль", callback_data=f'february|{user_id}')
        button3 = types.InlineKeyboardButton("Март", callback_data=f'march|{user_id}')
        button4 = types.InlineKeyboardButton("Апрель", callback_data=f'april|{user_id}')
        button5 = types.InlineKeyboardButton("Май", callback_data=f'may|{user_id}')
        button6 = types.InlineKeyboardButton("Июнь", callback_data=f'june|{user_id}')
        button7 = types.InlineKeyboardButton("Июль", callback_data=f'july|{user_id}')
        button8 = types.InlineKeyboardButton("Август", callback_data=f'august|{user_id}')
        button9 = types.InlineKeyboardButton("Сентябрь", callback_data=f'september|{user_id}')
        button10 = types.InlineKeyboardButton("Октябрь", callback_data=f'october|{user_id}')
        button11 = types.InlineKeyboardButton("Ноябрь", callback_data=f'november|{user_id}')
        button12 = types.InlineKeyboardButton("Декабрь", callback_data=f'december|{user_id}')
        markup.add(button1, button2, button3, button4, button5, button6,
                   button7, button8, button9, button10, button11, button12)
        bot.send_message(chat_id=message.chat.id, text="Выбери месяц:", reply_markup=markup)

    elif message.text == "Начать новый месяц" or msg == "Начать новый месяц":
        bot.send_message(chat_id=message.chat.id, text="В разработке.")

    else:
        bot.send_message(message.chat.id,
                         text=f"К сожалению я не смог распознать твою команду.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик. Обрабатывает запросы от кнопок из функции main().
    """
    try:
        user_id = call.data.split('|')[1]
        if call.message:
            if call.data.startswith('pervichka'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn="pervichka", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith('garant'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn="garant", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith('holod'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn="holod", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith('artem'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn="artem", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith('cleanmoney'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn="cleanmoney", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith('nonprofile'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn="nonprofile", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith(('january', 'february', 'march', 'april', 'may', 'june',
                                       'july', 'august', 'september', 'october', 'november', 'december')):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                total_salary = func.DatabaseData(msg=call.message,
                                                 user=user_id,
                                                 month=call.data.split('|')[0]
                                                 ).db_get_total_sum()
                if total_salary is not None:
                    bot.send_message(chat_id=call.message.chat.id,
                                     text=f"Сумма за {call.data.split('|')[0]}: {total_salary} рублей.")
                else:
                    bot.send_message(chat_id=call.message.chat.id, text=f"💾 Нет данных")
    except Exception as ex:
        bot.send_message(call.message.chat.id, text=f"Ошибка: {ex}")


if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception:
            bot.close()
            sleep(15)
            continue
