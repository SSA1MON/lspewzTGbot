import sqlite3
import telebot.types
import buttons as btn
import func

from telebot import types, TeleBot
from config import TOKEN
from settings_dict import month_dict, category_dict
from time import sleep

bot = TeleBot(token=TOKEN, parse_mode='Markdown')
conn = sqlite3.connect(database='database.db', check_same_thread=False)
cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    """
    Функция обработчик. Обрабатывает команду /start.

    Parameters:
        message (telebot.types.Message): Служебная переменная библиотеки telebot.
    Returns:
        None
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text=btn.check_salary)
    btn2 = types.KeyboardButton(text=btn.average_receipt)
    btn3 = types.KeyboardButton(text=btn.add_cash)
    markup.add(btn1, btn2, btn3)

    func.write_log(user_id=message.from_user.id, func_name=start.__name__, text="Начало работы с ботом")
    # создает дополнительную кнопку меню
    bot.set_my_commands([telebot.types.BotCommand("/start", "Перезапуск бота")])
    # создает таблицу в бд, если её нет
    func.DatabaseData(msg=message, user=message.from_user.id).db_update_month_column()
    bot.send_message(chat_id=message.chat.id, text=f"Wassup, *{message.from_user.first_name}*!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main(message: telebot.types.Message) -> None:
    """
    Функция обработчик сообщений. Обрабатывает команды от кнопок в меню, при начале диалога с ботом (/start)

    Parameters:
        message (telebot.types.Message): Служебная переменная библиотеки telebot.
    Returns:
        None
    """

    user_id = message.from_user.id
    if message.text == btn.add_cash:
        func.write_log(user_id=message.from_user.id, func_name=main.__name__,
                       text=f"Выбрана кнопка '{btn.add_cash}'")
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("Первичка", callback_data=f'{btn.pervichka}|{user_id}')
        btn2 = types.InlineKeyboardButton("Гарантия", callback_data=f'{btn.garant}|{user_id}')
        btn3 = types.InlineKeyboardButton("Холод", callback_data=f'{btn.holod}|{user_id}')
        btn4 = types.InlineKeyboardButton("ЗаявОЧКА", callback_data=f'{btn.zayavochka}|{user_id}')
        btn5 = types.InlineKeyboardButton("Чистые деньги", callback_data=f'{btn.clean_money}|{user_id}')
        btn6 = types.InlineKeyboardButton("Непрофиль", callback_data=f'{btn.non_profile}|{user_id}')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(chat_id=message.chat.id, text="Выбери нужную категорию 👇", reply_markup=markup)

    elif message.text == btn.check_salary:
        func.write_log(user_id=message.from_user.id, func_name=main.__name__,
                       text=f"Выбрана кнопка '{btn.check_salary}'")
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("Январь", callback_data=f'january|{user_id}')
        btn2 = types.InlineKeyboardButton("Февраль", callback_data=f'february|{user_id}')
        btn3 = types.InlineKeyboardButton("Март", callback_data=f'march|{user_id}')
        btn4 = types.InlineKeyboardButton("Апрель", callback_data=f'april|{user_id}')
        btn5 = types.InlineKeyboardButton("Май", callback_data=f'may|{user_id}')
        btn6 = types.InlineKeyboardButton("Июнь", callback_data=f'june|{user_id}')
        btn7 = types.InlineKeyboardButton("Июль", callback_data=f'july|{user_id}')
        btn8 = types.InlineKeyboardButton("Август", callback_data=f'august|{user_id}')
        btn9 = types.InlineKeyboardButton("Сентябрь", callback_data=f'september|{user_id}')
        btn10 = types.InlineKeyboardButton("Октябрь", callback_data=f'october|{user_id}')
        btn11 = types.InlineKeyboardButton("Ноябрь", callback_data=f'november|{user_id}')
        btn12 = types.InlineKeyboardButton("Декабрь", callback_data=f'december|{user_id}')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
        bot.send_message(chat_id=message.chat.id, text="Выбери месяц 👇", reply_markup=markup)

    elif message.text == btn.average_receipt:
        func.write_log(user_id=message.from_user.id, func_name=main.__name__,
                       text=f"Выбрана кнопка '{btn.average_receipt}'")
        data = func.DatabaseData(msg=message, user=user_id).db_calc_avg_sum()
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Твоя текущая категория — _{data[0]}_\n\nТвой текущий средний чек:   *{data[1]} RUB*"
        )

    else:
        func.write_log(user_id=user_id, func_name=main.__name__,
                       text=f"Ошибка распознования команды. Исполнен else. Введено: {message.text}")
        bot.send_message(chat_id=message.chat.id, text="К сожалению я не смог распознать твою команду.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик. Обрабатывает запросы от кнопок из функции main().

    Parameters:
        call (telebot.types.CallbackQuery): Cлужебная переменная библиотеки telebot. Получает данные от inline кнопок.
    Returns:
        None
    """

    try:
        value = call.data.split('|')[0]
        user_id = call.data.split('|')[1]
        selected_button = None

        if call.message:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

            # алгоритм inline кнопок внутри "Посмотреть ЗП"
            if value in month_dict.keys():
                total_salary = func.DatabaseData(msg=call.message, user=user_id, month=value).db_get_total_sum()
                month = month_dict.get(value)

                if total_salary is not None:
                    func.write_log(user_id=int(user_id), func_name=callback_inline.__name__,
                                   text="Вывод зп за " + month.upper())
                    bot.send_message(chat_id=call.message.chat.id,
                                     text=f"Цифры за *{month.upper()}:*\n\n"
                                          f"*⚡ Первичка:*            {total_salary[0][0]}\n"
                                          f"*⚡ Гарантия:*             {total_salary[0][1]}\n"
                                          f"*⚡ Холод:*                     {total_salary[0][2]}\n"
                                          f"*⚡ ЗаявОЧКА:*            {total_salary[0][3]}\n"
                                          f"*⚡ Чистые:*                   {total_salary[0][4]}\n"
                                          f"*⚡ Непрофиль:*         {total_salary[0][5]}\n\n"
                                          f"*ИТОГО:*     {total_salary[1]} RUB")
                else:
                    func.write_log(user_id=int(user_id), func_name=callback_inline.__name__,
                                   text="Нет данных за " + month.upper())
                    bot.send_message(chat_id=call.message.chat.id, text="💾 Нет данных")
                return None

            msg_text = f"Введи сумму для _{category_dict.get(value).upper()}_ 👇"

            if value == btn.pervichka:
                selected_button = btn.pervichka
            elif value == btn.garant:
                selected_button = btn.garant
            elif value == btn.holod:
                selected_button = btn.holod
            elif value == btn.zayavochka:
                selected_button = btn.zayavochka
                msg_text = f"Введи сумму для _{category_dict.get(value).upper()}_\n(в формате: _сумма процент_) 👇"
            elif value == btn.clean_money:
                selected_button = btn.clean_money
            elif value == btn.non_profile:
                selected_button = btn.non_profile

            msg = bot.send_message(call.message.chat.id, msg_text)

            func.DatabaseData(msg=call.message, button=selected_button, user=user_id).db_update_button()
            bot.register_next_step_handler(msg, func.answer_handler)

    except Exception as ex:
        bot.send_message(chat_id=call.message.chat.id, text=f"Ошибка в callback_inline: {ex}")


if __name__ == '__main__':
    while True:
        try:
            print("Bot is running...")
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception:
            bot.close()
            sleep(15)
            continue
