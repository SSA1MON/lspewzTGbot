import time
import math
import buttons

from typing import Union
from bot import cursor, conn, bot, main
from datetime import datetime

cur_month = datetime.now().strftime("%d-%B-%Y %H:%M").split('-')[1].lower()

month_dict = {
    'january': "январь", 'february': "февраль", 'march': 'март', 'april': "апрель", 'may': "май", 'june': "июнь",
    'july': 'июль', 'august': 'август', 'september': "сентябрь", 'october': "октябрь", 'november': "ноябрь",
    'december': "декабрь"
}


def db_table_val(month: str, perv: float, garant: float, holod: float,
                 artem: float, cleanmoney: float, nonprofile: float, curbtn: str, usr_id: int) -> None:
    """
    Функция. Создает таблицу в базе данных, если её нет и заполняет первоначальными данными, которые подаются на вход.
    """

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS salary '
        '(s_month STRING, s_pervichka REAL, s_garant REAL, s_holod REAL, s_artem REAL, '
        's_cleanmoney REAL, s_nonprofile REAL, s_curbtn STRING, usr_id INTEGER)'
    )
    cursor.execute(
        'INSERT INTO salary '
        '(s_month, s_pervichka, s_garant, s_holod, s_artem, s_cleanmoney, s_nonprofile, s_curbtn, usr_id) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
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

    # функция, добавляющая в бд кнопку выбранную пользователем
    def db_update_button(self) -> None:
        try:
            cursor.execute(f'UPDATE salary SET s_curbtn = "{self.button}" WHERE usr_id = {self.user_id}')
            conn.commit()
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id,
                             text=f"Что-то пошло не так при обновлении данных в БД.\nОшибка: {ex}")

    # функция получающая из бд информацию о кнопке выбранной пользователем
    def db_get_button(self) -> tuple[str, int]:
        try:
            cursor.execute(f"SELECT s_curbtn FROM salary WHERE usr_id = {self.user_id}")
            current_button = cursor.fetchall()[0][0]
            return current_button, self.user_id
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id,
                             text=f"Что-то пошло не так при обращении к БД.\nОшибка: {ex}")

    # функция получающая информацию из бд об имеющихся записях месяцев у пользователя
    # если записи нет, добавляет её
    def db_month_column(self) -> None:
        global cur_month
        cur_month = datetime.now().strftime("%d-%B-%Y %H:%M").split('-')[1].lower()

        cursor.execute(f"SELECT * FROM salary WHERE usr_id = {self.user_id}")
        db_data = cursor.fetchall()
        month_list = []

        for i_month in db_data:
            month_list.append(i_month[0])

        # cоздает таблицу с текущим месяцем в бд, если её нет
        if cur_month not in month_list:
            db_table_val(month=cur_month, perv=0, garant=0, holod=0, artem=0, cleanmoney=0,
                         nonprofile=0, curbtn="None", usr_id=self.user_id)

    # функция добавляющая вводимую пользователем сумму в бд
    def add_sum(self) -> None:
        try:
            self.db_month_column()
            cursor.execute(
                f"UPDATE salary SET {self.column} = {self.column} + {round(self.calc_sum, 2)} "
                f"WHERE s_month = '{self.month}' AND usr_id = {self.user_id}"
            )
            conn.commit()
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id,
                             text=f"Что-то пошло не так при обращении к БД.\nОшибка: {ex}")

    # функция получающая записи сумм из бд и суммирует их
    def db_get_total_sum(self) -> Union[tuple[tuple[float], float], None]:
        try:
            cursor.execute(
                "SELECT s_pervichka, s_garant, s_holod, s_artem, s_cleanmoney, s_nonprofile"
                f" FROM salary WHERE s_month = '{self.month}' AND usr_id = {self.user_id}"
            )
            db_data = cursor.fetchall()[0]
            total_sum = round(math.fsum(list(map(float, db_data))), 2)
            return db_data, total_sum  # возвращает кортеж всех сумм из бд и итоговую сумму
        except IndexError:
            return None
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id,
                             text=f"Что-то пошло не так при обращении к БД.\nОшибка: {ex}")


def answer_handler(message) -> None:
    db_data = DatabaseData(msg=message, user=message.from_user.id).db_get_button()
    button = db_data[0]
    user_id = db_data[1]

    column = ""
    percent = 0

    try:
        input_sum = float(message.text)
        float_sum = True

        if button == buttons.pervichka:
            column = "s_pervichka"
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

        elif button == buttons.garant or button == buttons.holod:
            if button == buttons.garant:
                column = 's_garant'
            elif button == buttons.holod:
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

        elif button == buttons.artem:
            column = "s_artem"
            input_sum *= 0.45
            percent = 45

        elif button == buttons.clean_money:
            percent = 100
            column = "s_cleanmoney"

        elif button == buttons.non_profile:
            column = "s_nonprofile"
            if 0 < input_sum <= 10500:
                input_sum *= 0.40
                percent = 40
            elif 10500 < input_sum <= 17000:
                input_sum *= 0.45
                percent = 45
            elif input_sum > 17000:
                input_sum *= 0.50
                percent = 50

        else:
            bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так... Обратись к разрабу.")

        # проверка на то, что input_sum - число и больше нуля. Если верно, то внесение данных в бд.
        if float_sum is True and input_sum > 0:
            DatabaseData(msg=message, user=user_id, summ=input_sum, column=column, month=cur_month).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"Сумма *{round(input_sum, 2)} RUB* ({percent}%) добавлена.")
        else:
            bot.send_message(chat_id=message.chat.id, text="Что-то у тебя с числом не так. Может быть оно меньше нуля?")
            time.sleep(0.7)
            message.text = buttons.add_cash
            main(message=message)

    except Exception:
        bot.send_message(chat_id=message.chat.id,
                         text="Что-то пошло не так при обработке введенных данных, либо это не число.")
        time.sleep(0.7)
        message.text = buttons.add_cash
        main(message=message)
