import sqlite3
import time

from telebot import types, TeleBot
from config import TOKEN
from time import sleep
from datetime import datetime

bot = TeleBot(TOKEN)
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(month: str, perv: float, garant: float, holod: float,
                 artem: float, cleanmoney: float, nonprofile: float, curbtn: str, usr_id: int):

    cursor.execute(f'CREATE TABLE IF NOT EXISTS salary (s_month STRING, s_pervichka REAL, '
                   's_garant REAL, s_holod REAL, s_artem REAL, s_cleanmoney REAL, s_nonprofile REAL, '
                   's_curbtn STRING, usr_id INTEGER)')
    cursor.execute(
        f'INSERT INTO salary (s_month, s_pervichka, s_garant, s_holod, '
        f's_artem, s_cleanmoney, s_nonprofile, s_curbtn, usr_id) '
        f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (month, perv, garant, holod, artem, cleanmoney, nonprofile, curbtn, usr_id)
    )
    conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("Добавить приход")
    btn2 = types.KeyboardButton("Посмотреть ЗП")
    btn3 = types.KeyboardButton("Начать новый месяц")
    markup.add(btn1, btn2, btn3)

    user_id = message.from_user.id
    cur_month = datetime.now().strftime("%d-%B-%Y %H:%M").split('-')[1].lower()
    db_table_val(month=cur_month, perv=0, garant=0, holod=0, artem=0, cleanmoney=0,
                 nonprofile=0, curbtn="None", usr_id=user_id)
    bot.send_message(message.chat.id,
                     text=f"Wassup, <b>{message.from_user.first_name}</b>!\n",
                     reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types=['text'])
def main(message, msg=None):
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
        bot.send_message(chat_id=message.chat.id, text="В разработке.")
    elif message.text == "Начать новый месяц" or msg == "Начать новый месяц":
        bot.send_message(chat_id=message.chat.id, text="В разработке.")
    else:
        bot.send_message(message.chat.id,
                         text=f"К сожалению я не смог распознать твою команду.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        user_id = call.data.split('|')[1]
        if call.message:
            if call.data.startswith('pervichka'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                DatabaseData(msg=call.message, btn="pervichka", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=answer_handler)
            elif call.data.startswith('garant'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                DatabaseData(msg=call.message, btn="garant", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=answer_handler)
            elif call.data.startswith('holod'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                DatabaseData(msg=call.message, btn="holod", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=answer_handler)
            elif call.data.startswith('artem'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                DatabaseData(msg=call.message, btn="artem", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=answer_handler)
            elif call.data.startswith('cleanmoney'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                DatabaseData(msg=call.message, btn="cleanmoney", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=answer_handler)
            elif call.data.startswith('nonprofile'):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                DatabaseData(msg=call.message, btn="nonprofile", user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=answer_handler)
    except Exception as ex:
        bot.send_message(call.message.chat.id, text=f"Ошибка: {ex}")


class DatabaseData:
    def __init__(self, msg, btn=None, user=None, summ=None, column=None):
        self.message = msg
        self.button = btn
        self.user_id = user
        self.column = column
        self.calc_sum = summ

    def db_update_button(self):
        try:
            cursor.execute(
                f'UPDATE salary SET s_curbtn = "{self.button}" WHERE usr_id = {self.user_id}'
            )
            conn.commit()
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=f"Что-то пошло не так при обновлении данных в БД. {ex}")

    def db_get_button(self):
        try:
            cursor.execute(
                f"SELECT s_curbtn FROM salary WHERE usr_id = {self.user_id}"
            )
            current_button = cursor.fetchall()[0][0]
            return current_button, self.user_id
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=f"Что-то пошло не так при обращении к БД. {ex}")

    def add_sum(self):
        cursor.execute(
            f'UPDATE salary SET {self.column} = {self.column} + {self.calc_sum} WHERE usr_id = {self.user_id}'
        )
        conn.commit()


def answer_handler(message):
    db_data = DatabaseData(msg=message, user=message.from_user.id).db_get_button()
    button = db_data[0]
    user_id = db_data[1]

    try:
        input_sum = float(message.text)
        if button == 'pervichka':
            if 0 < input_sum <= 2500:
                calc_sum = input_sum * 0.25
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"25% суммы внесено")
            elif 2500 < input_sum <= 4500:
                calc_sum = input_sum * 0.30
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"30% суммы внесено")
            elif 4500 < input_sum <= 7500:
                calc_sum = input_sum * 0.35
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"35% суммы внесено")
            elif 7500 < input_sum <= 10500:
                calc_sum = input_sum * 0.40
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"40% суммы внесено")
            elif 10500 < input_sum <= 17000:
                calc_sum = input_sum * 0.45
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"45% суммы внесено")
            elif input_sum > 17000:
                calc_sum = input_sum * 0.50
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"50% суммы внесено")
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Что-то у тебя с числом не так")
                time.sleep(0.7)
                main(message=message, msg="Добавить приход")
        elif button == 'garant' or button == 'holod':
            column = None
            if button == 'garant':
                column = 's_garant'
            elif button == 'holod':
                column = 's_holod'

            if 0 < input_sum <= 10500:
                calc_sum = input_sum * 0.50
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column=column).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"50% суммы внесено")
            elif 10500 < input_sum <= 17000:
                calc_sum = input_sum * 0.45
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column=column).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"45% суммы внесено")
            elif input_sum > 17000:
                calc_sum = input_sum * 0.50
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column=column).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"50% суммы внесено")
        elif button == 'artem':
            calc_sum = input_sum * 0.45
            DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_artem').add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"45% суммы внесено")
        elif button == 'cleanmoney':
            DatabaseData(msg=message, user=user_id, summ=input_sum, column='s_cleanmoney').add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"100% суммы внесено")
        elif button == 'nonprofile':
            if 0 < input_sum <= 10500:
                calc_sum = input_sum * 0.40
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_nonprofile').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"40% суммы внесено")
            elif 10500 < input_sum <= 17000:
                calc_sum = input_sum * 0.45
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_nonprofile').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"45% суммы внесено")
            elif input_sum > 17000:
                calc_sum = input_sum * 0.50
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_nonprofile').add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"50% суммы внесено")
        else:
            bot.send_message(chat_id=message.chat.id, text=f"Что-то пошло не так... Обратись к разрабу.")
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Что-то пошло не так при введении суммы\n{ex}")


if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception:
            bot.close()
            sleep(15)
            continue
