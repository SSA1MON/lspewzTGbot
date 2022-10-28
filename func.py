import time
import math

from bot import cursor, conn, bot, main, cur_month


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

    def add_sum(self):
        try:
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
            if 0 < input_sum <= 2500:
                calc_sum = input_sum * 0.25
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka', month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"25% суммы внесено")
            elif 2500 < input_sum <= 4500:
                calc_sum = input_sum * 0.30
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka', month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"30% суммы внесено")
            elif 4500 < input_sum <= 7500:
                calc_sum = input_sum * 0.35
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka', month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"35% суммы внесено")
            elif 7500 < input_sum <= 10500:
                calc_sum = input_sum * 0.40
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka', month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"40% суммы внесено")
            elif 10500 < input_sum <= 17000:
                calc_sum = input_sum * 0.45
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka', month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"45% суммы внесено")
            elif input_sum > 17000:
                calc_sum = input_sum * 0.50
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_pervichka', month=cur_month).add_sum()
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
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column=column, month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"50% суммы внесено")
            elif 10500 < input_sum <= 17000:
                calc_sum = input_sum * 0.45
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column=column, month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"45% суммы внесено")
            elif input_sum > 17000:
                calc_sum = input_sum * 0.50
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column=column, month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"50% суммы внесено")
        elif button == 'artem':
            calc_sum = input_sum * 0.45
            DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_artem', month=cur_month).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"45% суммы внесено")
        elif button == 'cleanmoney':
            DatabaseData(msg=message, user=user_id, summ=input_sum, column='s_cleanmoney', month=cur_month).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"100% суммы внесено")
        elif button == 'nonprofile':
            if 0 < input_sum <= 10500:
                calc_sum = input_sum * 0.40
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_nonprofile', month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"40% суммы внесено")
            elif 10500 < input_sum <= 17000:
                calc_sum = input_sum * 0.45
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_nonprofile', month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"45% суммы внесено")
            elif input_sum > 17000:
                calc_sum = input_sum * 0.50
                DatabaseData(msg=message, user=user_id, summ=calc_sum, column='s_nonprofile', month=cur_month).add_sum()
                bot.send_message(chat_id=message.chat.id, text=f"50% суммы внесено")
        else:
            bot.send_message(chat_id=message.chat.id, text=f"Что-то пошло не так... Обратись к разрабу.")
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Что-то пошло не так при введении суммы\n{ex}")