import sqlite3
import os
import time
import math
import buttons as btn

from typing import Union, Optional
from bot import cursor, conn, bot, main, types
from settings_dict import percent_rates
from datetime import datetime

cur_month = datetime.now().strftime("%B").lower()


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
            '(s_month STRING, s_pervichka REAL, s_garant REAL, s_holod REAL, s_zayavochka REAL, '
            's_cleanmoney REAL, s_nonprofile REAL, s_allsum REAL, s_curbtn STRING, s_class STRING, s_count INTEGER)'
        )
        cursor.execute(
            f'INSERT INTO [{usr_id}] '
            '(s_month, s_pervichka, s_garant, s_holod, s_zayavochka, s_cleanmoney, s_nonprofile, s_allsum, s_curbtn, '
            's_class, s_count)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (cur_month, 0, 0, 0, 0, 0, 0, 0, None, "B", 0)
        )
        conn.commit()
        write_log(user_id=usr_id, func_name=db_table_val.__name__, text=f"База данных создана.")
    except sqlite3.OperationalError as err:
        write_log(user_id=usr_id, func_name=db_table_val.__name__, text=f"Ошибка при работе с БД. {err}")
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
    def __init__(self, msg: types.Message, button: str = None, user: Union[str, int] = None,
                 month: str = None, summ: list[float, float] = None, column: str = None,
                 cls: str = None) -> None:
        """
        Создает все необходимые атрибуты для объекта DatabaseData.

        Parameters:
            msg (telebot.types.Message): Служебная переменная библиотеки telebot.
            button (str): Текущая выбранная пользователем inline кнопка.
            user (str/int): Идентификатор пользователя.
            month (str): Месяц, выбранный пользователем. Используется для просмотра ЗП по месяцам.
            summ (list): Список чисел [float, float]. Введённое пользователем и высчитанный чистый процент.
            column (str): Наименование столбца в БД. Используется для указания вводимых данных в БД.
            cls (str): Выбранная пользователем категория (класс).

        Returns:
            None
        """

        self.message = msg
        self.button = button
        self.user_id = user
        self.column = column
        self.calc_sum = summ
        self.month = month
        self.selected_class = cls
        self.err_text = f"⚠ Что-то пошло не так при обращении к БД.\nОшибка: "

    def db_update_button(self) -> None:
        """
        Функция. Обновляет в БД данные о выбранной пользователем inline кнопке в текущем месяце.

        Returns:
            None
        """

        try:
            cursor.execute(f'UPDATE [{self.user_id}] SET s_curbtn = "{self.button}" WHERE s_month = "{cur_month}"')
            conn.commit()
            write_log(user_id=self.user_id, func_name=self.db_update_button.__name__,
                      text="Обновлена inline кнопка в БД")
        except Exception as ex:
            write_log(user_id=self.user_id, func_name=self.db_update_button.__name__, text=self.err_text + str(ex))
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    def db_get_button(self) -> Union[tuple[str], None]:
        """
        Функция. Получает из БД данные об inline кнопке, выбранной пользователем в текущем месяце и
        возвращает кортеж значений.

        Returns:
            current_button (str): Наименование inline кнопки
        """

        try:
            cursor.execute(f"SELECT s_curbtn FROM [{self.user_id}] WHERE s_month = '{cur_month}'")
            current_button = cursor.fetchall()[0][0]
            write_log(user_id=self.user_id, func_name=self.db_get_button.__name__,
                      text="Получена inline кнопка из БД")
            return current_button
        except Exception as ex:
            write_log(user_id=self.user_id, func_name=self.db_get_button.__name__, text=self.err_text + str(ex))
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
            write_log(user_id=self.user_id, func_name=self.db_update_class.__name__,
                      text="Обновлена категория юзера в БД")
        except Exception as ex:
            write_log(user_id=self.user_id, func_name=self.db_update_class.__name__, text=self.err_text + str(ex))
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
            write_log(user_id=self.user_id, func_name=self.db_get_class.__name__,
                      text="Получена категория юзера из БД")
            return current_class
        except Exception as ex:
            write_log(user_id=self.user_id, func_name=self.db_get_class.__name__, text=self.err_text + str(ex))
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    def db_check_class(self) -> None:
        """
        Функция. Получает категорию (класс) пользователя из БД.
        Вызывает функцию db_update_class и изменяет категорию, если будут выполнены условия в теле функции.

        Returns:
            None
        """

        db_data = self.db_calc_avg_sum()
        cur_class = db_data[0]     # текущая категория
        avg_sum = db_data[1]   # текущий средний чек

        if avg_sum <= 5500 and cur_class == btn.class_a:
            self.selected_class = btn.class_b
            self.db_update_class()
        elif avg_sum > 5500 and cur_class == btn.class_b:
            self.selected_class = btn.class_a
            self.db_update_class()

    def db_update_month_column(self) -> None:
        """
        Функция. Получает все записи s_month из БД. Проверяет наличие текущего месяца в полученном кортеже и
        если такогово нет, вызывает функцию db_table_val, в которой создается новая запись.
        Так же обновляет данные текущего месяца в глобальной переменной cur_month.

        Returns:
            None
        """

        global cur_month
        cur_month = datetime.now().strftime("%B").lower()
        month_list = list()

        try:
            cursor.execute(f"SELECT s_month FROM [{self.user_id}]")
            db_data = cursor.fetchall()
            month_list = [i[0] for i in db_data]
        except sqlite3.OperationalError:
            pass

        if cur_month not in month_list:
            db_table_val(usr_id=self.user_id)

    def db_update_add_sum(self) -> None:
        """
        Функция. Вносит в БД значения введенные пользователем.

        Добавляет в выбранную пользователем колонку полученный аргумент содержащий число,
        прибавляет в счетчик заявок (s_count) единицу, если условие выполняется и вносит
        исходное число полученное от пользователя в колонку среднего чека (s_allsum).

        Returns:
            None
        """

        try:
            self.db_update_month_column()
            count, original_sum = 0, 0

            # условия внесения данных для подсчета среднего чека
            if self.column in ['s_pervichka', 's_garant', 's_holod']:
                if self.column == 's_pervichka':
                    count = 1
                elif self.calc_sum[0] > 10500 and self.column in ['s_garant', 's_holod']:
                    count = 1
                original_sum = round(self.calc_sum[0], 2)
            elif self.calc_sum[0] > 7500 and self.column == 's_nonprofile':
                count = 1
                original_sum = round(self.calc_sum[0], 2)

            cursor.execute(
                f"UPDATE [{self.user_id}] SET {self.column} = {self.column} + {round(self.calc_sum[1], 2)}, "
                f"s_count = s_count + {count}, s_allsum = s_allsum + {original_sum} WHERE s_month = '{cur_month}'"
            )
            conn.commit()
            write_log(user_id=self.user_id, func_name=self.db_update_add_sum.__name__,
                      text="Обновлены значения в БД.")
            self.db_check_class()
        except Exception as ex:
            write_log(user_id=self.user_id, func_name=self.db_update_add_sum.__name__, text=self.err_text + str(ex))
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
                "SELECT s_pervichka, s_garant, s_holod, s_zayavochka, s_cleanmoney, s_nonprofile"
                f" FROM [{self.user_id}] WHERE s_month = '{self.month}'"
            )
            db_data = cursor.fetchall()[0]
            total_sum = round(math.fsum(list(map(float, db_data))), 2)
            write_log(user_id=self.user_id, func_name=self.db_get_total_sum.__name__,
                      text="Просуммированы имеющиеся в БД суммы")
            return db_data, total_sum  # возвращает кортеж всех сумм из бд и итоговую сумму
        except IndexError:
            return
        except Exception as ex:
            write_log(user_id=self.user_id, func_name=self.db_get_total_sum.__name__, text=self.err_text + str(ex))
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))

    def db_calc_avg_sum(self) -> Union[tuple[str, float], None]:
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

            write_log(user_id=self.user_id, func_name=self.db_calc_avg_sum.__name__,
                      text="Посчитано среднее значение в чеке")
            return current_class, average_sum

        except Exception as ex:
            write_log(user_id=self.user_id, func_name=self.db_calc_avg_sum.__name__, text=self.err_text + str(ex))
            bot.send_message(chat_id=self.message.chat.id, text=self.err_text + str(ex))


def write_log(user_id: int, func_name: str, text: str) -> None:
    """
    Функция логгер. Создает и записывает в файл с именем id пользователя полученные данные.

    Parameters:
        user_id (int): Идентификатор пользователя.
        func_name (str): Название функции из которой вызывается логгер.
        text (str): Текст для записи в файл.
    """

    current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    try:

        if os.path.exists('logs') is False:
            os.mkdir('logs')
        if os.path.exists('logs/' + str(user_id) + '.log') is False:
            with open('logs/' + str(user_id) + '.log', 'w', encoding='utf-8') as create_file:
                create_file.write(f"{current_time} | {func_name} | {text}.")
            return

        with open('logs/' + str(user_id) + '.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"\n{current_time} | {func_name} | {text}.")

    except FileExistsError:
        return
    except Exception as ex:
        print(ex)


def calc_salary(user_id: int, user_sum: float, user_btn: str, user_class: str) -> Optional[tuple[float, str, str]]:
    """
    Функция. Считает процент от введенной суммы пользователем.
    Получает из словаря название колонки и проценты в зависимости от категории (класса)
    пользователя, считает процент и возвращает результат.

    Parameters:
        user_id (int): Идентификатор пользователя.
        user_sum (float): Число полученное от пользователя.
        user_btn (str): Название кнопки выбранной пользователем.
        user_class (str): Текущая категория (класс) пользователя.

    Returns:
        calc_num (float): Результат деления суммы на процент от категории и кнопки пользователя.
        rate (int): Процент, используемый для текстового вывода.
        column (str): Название колонки в базе данных для внесения результата.
    """
    try:
        column = percent_rates.get(user_class).get(user_btn).get('column_name')
        rate_dict = percent_rates.get(user_class).get(user_btn).get('rate')
        rate_keys = list(rate_dict.keys())
        rate = rate_dict.get(rate_keys[-1]) if user_sum >= rate_keys[-1] else None

        if rate is None:
            for i in rate_keys:
                if user_sum <= i:
                    rate = rate_dict.get(i)
                    break
                else:
                    continue

        calc_num = round(user_sum * (rate / 100), 2)
        return calc_num, rate, column
    except Exception as ex:
        write_log(user_id=user_id, func_name=calc_salary.__name__, text=str(ex))


def calc_zayavochka(message):
    try:
        message.text = message.text.split(' ')
        if len(message.text) > 2:
            raise Exception
        user_sum = float(message.text[0])
        user_percent = float(message.text[1])
        calc_num = round(user_sum * (user_percent / 100), 2)
        return calc_num, user_sum, user_percent
    except Exception:
        return


def answer_handler(message: types.Message):
    """
    Функция обработчик. Обрабатывает введённые суммы от пользователя.

    Parameters:
        message (telebot.types.Message): Служебная переменная библиотеки telebot.

    Returns:
        None
    """

    user_id = message.from_user.id
    current_class = str(DatabaseData(msg=message, user=user_id).db_get_class())  # получение инфы о категории из бд
    button = str(DatabaseData(msg=message, user=user_id).db_get_button())  # получение инфы о кнопке из бд
    input_sum = message.text
    column = str()
    percent, calc_sum, = 0, 0
    float_sum = False

    if button in [btn.pervichka, btn.garant, btn.holod, btn.clean_money, btn.non_profile]:
        try:
            input_sum = float(input_sum)
            float_sum = True
        except ValueError:
            bot.send_message(
                chat_id=message.chat.id,
                text="❌ Что-то пошло не так при обработке введённых данных. Может быть это не число?"
            )
            time.sleep(0.7)
            message.text = btn.add_cash
            main(message=message)
            return

        result = calc_salary(user_id=user_id, user_sum=input_sum, user_btn=button, user_class=current_class)
        if result is not None:
            column = result[2]
            calc_sum = result[0]
            percent = result[1]
        else:
            return

    elif button == btn.zayavochka:
        column = 's_' + btn.zayavochka
        result = calc_zayavochka(message)
        if result is not None:
            float_sum = True
            calc_sum = result[0]
            input_sum = result[1]
            percent = result[2]

    else:
        write_log(user_id=user_id, func_name=answer_handler.__name__, text="Ошибка. Выполнился блок else.")
        bot.send_message(chat_id=message.chat.id, text="⚠ Что-то пошло не так... Обратись к разрабу.")

    # проверка, что input_sum - число и больше нуля. Если верно, то внесение данных в бд.
    if float_sum is True and input_sum > 0:
        DatabaseData(msg=message, user=user_id, summ=[input_sum, calc_sum], column=column).db_update_add_sum()
        bot.send_message(chat_id=message.chat.id, text=f"✅ Сумма *{round(calc_sum, 2)} RUB* ({percent}%) добавлена.",
                         reply_to_message_id=message.message_id)
    else:
        write_log(user_id=user_id, func_name=answer_handler.__name__, text="Ошибка. Выполнился блок else.")
        bot.send_message(chat_id=message.chat.id, text="❌ Что-то у тебя с числом не так.")
        time.sleep(0.7)
        message.text = btn.add_cash
        main(message=message)
