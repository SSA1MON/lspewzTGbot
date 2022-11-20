import sqlite3
import time
import math
import buttons

from typing import Union
from bot import cursor, conn, bot, main, types
from datetime import datetime

cur_month = datetime.now().strftime("%d-%B-%Y %H:%M").split('-')[1].lower()

month_dict = {
    'january': "январь", 'february': "февраль", 'march': 'март', 'april': "апрель", 'may': "май", 'june': "июнь",
    'july': 'июль', 'august': 'август', 'september': "сентябрь", 'october': "октябрь", 'november': "ноябрь",
    'december': "декабрь"
}


def db_table_val(usr_id: int) -> None:
    """
    Функция. Создает таблицу в базе данных, если её нет и
    заполняет дефолтными первоначальными данными, либо которые подаются на вход.

    Parameters:
        usr_id (int): Идентификатор пользователя

    Returns:
         None
    """

    try:
        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS [{usr_id}] '
            '(s_month STRING, s_pervichka REAL, s_garant REAL, s_holod REAL, s_artem REAL, '
            's_cleanmoney REAL, s_nonprofile REAL, s_allsum REAL, s_curbtn STRING, s_class STRING, s_count INTEGER)'
        )
        cursor.execute(
            f'INSERT INTO [{usr_id}] '
            '(s_month, s_pervichka, s_garant, s_holod, s_artem, s_cleanmoney, s_nonprofile, s_allsum, s_curbtn, '
            's_class, s_count)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (cur_month, 0, 0, 0, 0, 0, 0, 0, None, "B", 0)
        )
        conn.commit()
    except sqlite3.OperationalError as err:
        bot.send_message(chat_id=f"Что-то пошло не так при обращении к БД.\nОшибка: {err}")


class DatabaseData:
    """
    Класс. Представляющий работу с базой данных.

    Methods:
        db_update_button(): Обновляет информацию в БД о выбранной кнопке пользователем.
        db_get_button(): Получает информацию из БД о выбранной кнопке пользователем.
        db_get_class(): Получает информацию из БД о текущей категории (классе) пользователя.
        db_update_class(): Обновляет данные о категории (классе) в БД в текущем месяце.
        db_check_class(): Проверяет средний чек и категорию. Обновляет данные о категории в БД на актуальные.
    """
    def __init__(self, msg: types.Message, btn: str = None, user: Union[str, int] = None,
                 month: str = None, summ: list[float, float] = None, column: str = None,
                 cls: str = None) -> None:
        """
        Создает все необходимые атрибуты для объекта DatabaseData.

        Parameters:
            msg (telebot.types.Message): Служебная переменная библиотеки telebot.
            btn (str): Текущая выбранная пользователем inline кнопка.
            user (str/int): Идентификатор пользователя.
            month (str): Месяц, выбранный пользователем. Используется для просмотра ЗП по месяцам.
            summ (list): Список чисел [float, float]. Введённое пользователем и высчитанный чистый процент.
            column (str): Наименование столбца в БД. Используется для указания вводимых данных в БД.
            cls (str): Выбранная пользователем категория (класс).

        Returns:
            None
        """

        self.message = msg
        self.button = btn
        self.user_id = user
        self.column = column
        self.calc_sum = summ
        self.month = month
        self.selected_class = cls
        self.err_text = f"Что-то пошло не так при обращении к БД.\nОшибка: "

    def db_update_button(self) -> None:
        """
        Функция. Обновляет в БД данные о выбранной пользователем inline кнопке в текущем месяце.

        Returns:
            None
        """

        try:
            cursor.execute(f'UPDATE [{self.user_id}] SET s_curbtn = "{self.button}" WHERE s_month = "{cur_month}"')
            conn.commit()
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    def db_get_button(self) -> Union[tuple[str, int], None]:
        """
        Функция. Получает из БД данные об inline кнопке, выбранной пользователем в текущем месяце и
        возвращает кортеж значений.

        Returns:
            current_button (str): Наименование inline кнопки
            self.user_id (int): Идентификатор пользователя
        """

        try:
            cursor.execute(f"SELECT s_curbtn FROM [{self.user_id}] WHERE s_month = '{cur_month}'")
            current_button = cursor.fetchall()[0][0]
            return current_button, self.user_id
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    # получает значение категории пользователя из БД
    def db_get_class(self) -> Union[str, None]:
        """
        Функция. Получает значение категории (классе) пользователя из БД в текущем месяце.

        Returns:
            current_class (str): Информация о текущей категории (классе) из БД.
        """

        try:
            cursor.execute(f"SELECT s_class FROM [{self.user_id}] WHERE s_month = '{cur_month}'")
            current_class = cursor.fetchall()[0][0]
            return current_class
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    def db_update_class(self) -> None:
        """
        Функция. Обновляет данные о категории (классе) в БД в текущем месяце.

        Returns:
            None
        """

        try:
            cursor.execute(
                f"UPDATE [{self.user_id}] SET s_class = '{self.selected_class}' WHERE s_month = '{cur_month}'"
            )
            conn.commit()
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    def db_check_class(self) -> None:
        """
        Функция. Получает категорию (класс) пользователя из БД.
        Вызывает функцию db_update_class и изменяет категорию, если будут выполнены условия в теле функции.

        Returns:
            None
        """

        db_data = self.db_average_sum()
        cur_class = db_data[0]     # текущая категория
        avg_sum = db_data[1]   # текущий средний чек

        if avg_sum <= 5500 and cur_class == buttons.class_a:
            self.selected_class = buttons.class_b
            self.db_update_class()
        elif avg_sum > 5500 and cur_class == buttons.class_b:
            self.selected_class = buttons.class_a
            self.db_update_class()

    def db_month_column(self) -> None:
        """
        Функция. Получает все записи s_month из БД. Проверяет наличие текущего месяца в полученном кортеже и
        если такогово нет, вызывает функцию db_table_val, в которой создается новая запись.
        Так же обновляет данные текущего месяца в глобальной переменной cur_month.

        Returns:
            None
        """

        global cur_month
        cur_month = datetime.now().strftime("%d-%B-%Y %H:%M").split('-')[1].lower()
        db_data = list()

        try:
            cursor.execute(f"SELECT s_month FROM [{self.user_id}]")
            db_data = cursor.fetchall()
            return db_data
        except sqlite3.OperationalError:
            pass

        if cur_month not in db_data:
            db_table_val(usr_id=self.user_id)

    def add_sum(self) -> None:
        """
        Функция. Вносит в БД значения введенные пользователем.

        Добавляет в выбранную пользователем колонку полученный аргумент содержащий число,
        прибавляет в счетчик заявок (s_count) единицу, если условие выполняется и вносит
        исходное число полученное от пользователя в колонку среднего чека (s_allsum).

        Returns:
            None
        """

        try:
            self.db_month_column()
            count, original_sum = 0, 0

            # условия для подсчета среднего чека
            if self.column in ['s_pervichka', 's_garant', 's_holod']:
                if self.column == 's_pervichka':
                    count = 1
                original_sum = self.calc_sum[0]

            cursor.execute(
                f"UPDATE [{self.user_id}] SET {self.column} = {self.column} + {round(self.calc_sum[1], 2)}, "
                f"s_count = s_count + {count}, s_allsum = s_allsum + {original_sum} WHERE s_month = '{cur_month}'"
            )
            conn.commit()
            self.db_check_class()
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    def db_get_total_sum(self) -> Union[tuple[tuple[float], float], None]:
        """
        Функция. Суммирует суммы пользователя находящихся в БД.

        Получает все колонки с информацией о суммах из базы данных и суммирует их.

        Returns:
            db_data (tuple): Кортеж всех чисел, полученных из БД.
            total_sum (float): Сумма чисел из кортежа.
        """

        try:
            cursor.execute(
                "SELECT s_pervichka, s_garant, s_holod, s_artem, s_cleanmoney, s_nonprofile"
                f" FROM [{self.user_id}] WHERE s_month = '{self.month}'"
            )
            db_data = cursor.fetchall()[0]
            total_sum = round(math.fsum(list(map(float, db_data))), 2)
            return db_data, total_sum  # возвращает кортеж всех сумм из бд и итоговую сумму
        except IndexError:
            return
        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    def db_average_sum(self) -> Union[tuple[str, float], None]:
        """
        Функция. Высчитывает среднее значение в чеке по заданному условию.

        Получает колонки текущего месяца из БД, которые учавствуют в подсчете среднего чека,
        категорию (класс) пользователя, количество заявок и исходную сумму из всех чеков.
        Высчитывает среднее арифметическое между суммы всех чеков и количеством заявок.

        Returns:
            current_class (str): Текущая категория (класс) пользователя.
            average_sum (float): Исходная сумма всех чеков.
        """

        try:
            cursor.execute(
                f"SELECT s_pervichka, s_garant, s_holod, s_class, s_count, s_allsum "
                f"FROM [{self.user_id}] WHERE s_month = '{cur_month}'"
            )

            db_data = cursor.fetchall()[0]
            current_class = db_data[3]
            applications_num = db_data[4]
            average_sum = db_data[5]

            try:
                average_sum = round(average_sum / applications_num, 2)
            except ZeroDivisionError:
                average_sum = round(average_sum / 1, 2)
            return current_class, average_sum

        except Exception as ex:
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))


def answer_handler(message) -> None:
    """
    Функция обработчик. Обрабатывает введённые суммы от пользователя.

    Parameters:
        message (telebot.types.Message): Служебная переменная библиотеки telebot.

    Returns:
        None
    """

    db_data = DatabaseData(msg=message, user=message.from_user.id).db_get_button()
    button = db_data[0]
    user_id = db_data[1]

    current_class = DatabaseData(msg=message, user=user_id).db_get_class()
    column = ""
    percent = 0

    try:
        input_sum = float(message.text)
        calc_sum = 0
        float_sum = True

        if button == buttons.pervichka:
            column = "s_pervichka"
            if 0 < input_sum <= 2500:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .25
                    percent = 25
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .2
                    percent = 20
            elif 2500 < input_sum <= 4500:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .3
                    percent = 30
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .25
                    percent = 25
            elif 4500 < input_sum <= 7500:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .35
                    percent = 35
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .3
                    percent = 30
            elif 7500 < input_sum <= 10500:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .4
                    percent = 40
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .35
                    percent = 35
            elif 10500 < input_sum <= 17000:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .45
                    percent = 45
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .4
                    percent = 40
            elif input_sum > 17000:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .5
                    percent = 50
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .45
                    percent = 45

        elif button in [buttons.garant, buttons.holod]:
            if button == buttons.garant:
                column = 's_garant'
            elif button == buttons.holod:
                column = 's_holod'

            if 0 < input_sum <= 10500:
                calc_sum = input_sum * .5
                percent = 50
            elif 10500 < input_sum <= 17000:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .45
                    percent = 45
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .4
                    percent = 40
            elif input_sum > 17000:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .5
                    percent = 50
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .45
                    percent = 45

        elif button == buttons.artem:
            column = "s_artem"
            calc_sum = input_sum * .45
            percent = 45

        elif button == buttons.clean_money:
            percent = 100
            column = "s_cleanmoney"

        elif button == buttons.non_profile:
            column = "s_nonprofile"
            if 0 < input_sum <= 10500:
                calc_sum = input_sum * .4
                percent = 40
            elif 10500 < input_sum <= 17000:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .45
                    percent = 45
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .4
                    percent = 40
            elif input_sum > 17000:
                if current_class == buttons.class_a:
                    calc_sum = input_sum * .5
                    percent = 50
                elif current_class == buttons.class_b:
                    calc_sum = input_sum * .45
                    percent = 45

        else:
            bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так... Обратись к разрабу.")

        # проверка, что input_sum - число и больше нуля. Если верно, то внесение данных в бд.
        if float_sum is True and input_sum > 0:
            DatabaseData(msg=message, user=user_id, summ=[input_sum, calc_sum], column=column).add_sum()
            bot.send_message(chat_id=message.chat.id, text=f"Сумма *{round(calc_sum, 2)} RUB* ({percent}%) добавлена.")
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
