import time
import math

from bot import cursor, conn, bot, main
from datetime import datetime

cur_month = datetime.now().strftime("%d-%B-%Y %H:%M").split('-')[1].lower()


def db_table_val(month: str, perv: float, garant: float, holod: float,
                 artem: float, cleanmoney: float, nonprofile: float, curbtn: str, usr_id: int) -> None:
    """
    Функция. Создает таблицу в базе данных, если её нет и заполняет первоначальными данными.
    """

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


class DatabaseData:
    def __init__(self, msg, btn=None, user=None, summ=None, column=None, month=None):
        self.message = msg
        self.button = btn
        self.user_id = user
        self.column = column
        self.calc_sum = summ
        self.month = month

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

    def db_get_month_column(self):
        cursor.execute(f"SELECT * FROM salary WHERE usr_id = {self.user_id}")
        db_data = cursor.fetchall()
        month_list = []
        for i_month in db_data:
            month_list.append(i_month[0])
        if cur_month not in month_list:
            db_table_val(month=cur_month, perv=0, garant=0, holod=0, artem=0, cleanmoney=0,
                         nonprofile=0, curbtn="None", usr_id=self.user_id)

    def add_sum(self):
        try:
            self.db_get_month_column()
            cursor.execute(
                f"UPDATE salary SET {self.column} = {self.column} + {self.calc_sum} "
                f"WHERE s_month = '{self.month}' AND usr_id = {self.user_id}"
            )
            conn.commit()
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=f"Что-то пошло не так при обращении к БД. {ex}")

    def db_get_total_sum(self):
        try:
            cursor.execute(
                f"SELECT s_pervichka, s_garant, s_holod, s_artem, s_cleanmoney, s_nonprofile"
                f" FROM salary WHERE s_month = '{self.month}' AND usr_id = {self.user_id}"
            )
            db_data = cursor.fetchall()[0]
            db_data = round(math.fsum(list(map(float, db_data))), 2)
            return db_data
        except IndexError:
            return None
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=f"Что-то пошло не так при обращении к БД. {ex}")


def answer_handler(message):
    db_data = DatabaseData(msg=message, user=message.from_user.id).db_get_button()
    button = db_data[0]
    user_id = db_data[1]

    try:
        input_sum = float(message.text)
        if button == 'pervichka':
            percent = 0
            if 0 < input_sum <= 2500:
                input_sum *= 0.25
                percent = 25
            elif 2500 < input_sum <= 4500:
                input_sum *= 0.30
                percent = 30
            elif 4500 < input_sum <= 7500:
                input_sum *= 0.35
                percent = 35
            elif 7500 < input_sum <= 10500:
                input_sum *= 0.40
                percent = 40
            elif 10500 < input_sum <= 17000:
                input_sum *= 0.45
                percent = 45
            elif input_sum > 17000:
                input_sum *= 0.50
                percent = 50
            else:
                bot.send_message(chat_id=message.chat.id, text=f"Что-то у тебя с числом не так")
                time.sleep(0.7)
                main(message=message, msg="Добавить приход")
            DatabaseData(msg=message, user=user_id, summ=input_sum, column='s_pervichka', month=cur_month).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"Сумма {round(input_sum, 2)} ({percent}%) добавлена.")
        elif button == 'garant' or button == 'holod':
            column = None
            percent = 0
            if button == 'garant':
                column = 's_garant'
            elif button == 'holod':
                column = 's_holod'

            if 0 < input_sum <= 10500:
                input_sum *= 0.50
                percent = 50
            elif 10500 < input_sum <= 17000:
                input_sum *= 0.45
                percent = 45
            elif input_sum > 17000:
                input_sum *= 0.50
                percent = 50
            DatabaseData(msg=message, user=user_id, summ=input_sum, column=column, month=cur_month).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"Сумма {round(input_sum, 2)} ({percent}%) добавлена.")
        elif button == 'artem':
            input_sum *= 0.45
            DatabaseData(msg=message, user=user_id, summ=input_sum, column='s_artem', month=cur_month).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"Сумма {round(input_sum, 2)} (45%) добавлена.")
        elif button == 'cleanmoney':
            DatabaseData(msg=message, user=user_id, summ=input_sum, column='s_cleanmoney', month=cur_month).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"Сумма {round(input_sum, 2)} (100%) добавлена.")
        elif button == 'nonprofile':
            percent = 0
            if 0 < input_sum <= 10500:
                input_sum *= 0.40
                percent = 40
            elif 10500 < input_sum <= 17000:
                input_sum *= 0.45
                percent = 45
            elif input_sum > 17000:
                input_sum *= 0.50
                percent = 50
            DatabaseData(msg=message, user=user_id, summ=input_sum, column='s_nonprofile', month=cur_month).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"Сумма {round(input_sum, 2)} ({percent}%) добавлена.")
        else:
            bot.send_message(chat_id=message.chat.id, text=f"Что-то пошло не так... Обратись к разрабу.")
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Что-то пошло не так при введении суммы.\n\n{ex}")
