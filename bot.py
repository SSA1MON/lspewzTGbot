import sqlite3
import telebot.types
import buttons
import func

from telebot import types, TeleBot
from config import TOKEN
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
    btn1 = types.KeyboardButton(text=buttons.check_salary)
    btn2 = types.KeyboardButton(text=buttons.average_receipt)
    btn3 = types.KeyboardButton(text=buttons.add_cash)
    markup.add(btn1, btn2, btn3)

    # создает дополнительную кнопку меню
    bot.set_my_commands([telebot.types.BotCommand("/start", "Перезапуск бота")])
    # создает таблицу в бд, если её нет
    func.DatabaseData(msg=message, user=message.from_user.id).db_update_month_column()
    bot.send_message(chat_id=message.chat.id, text=f"Wassup, *{message.from_user.first_name}*!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main(message: telebot.types.Message) -> None:
    """
    Функция обработчик. Обрабатывает команды от кнопок в меню, при начале диалога с ботом (/start)

    Parameters:
        message (telebot.types.Message): Служебная переменная библиотеки telebot.

    Returns:
        None
    """

    user_id = message.from_user.id
    if message.text == buttons.add_cash:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("Первичка", callback_data=f'{buttons.pervichka}|{user_id}')
        btn2 = types.InlineKeyboardButton("Гарантия", callback_data=f'{buttons.garant}|{user_id}')
        btn3 = types.InlineKeyboardButton("Холод", callback_data=f'{buttons.holod}|{user_id}')
        btn4 = types.InlineKeyboardButton("Артём", callback_data=f'{buttons.artem}|{user_id}')
        btn5 = types.InlineKeyboardButton("Чистые деньги", callback_data=f'{buttons.clean_money}|{user_id}')
        btn6 = types.InlineKeyboardButton("Непрофиль", callback_data=f'{buttons.non_profile}|{user_id}')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(chat_id=message.chat.id, text="Выбери нужную категорию 👇", reply_markup=markup)

    elif message.text == buttons.check_salary:
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

    elif message.text == buttons.average_receipt:
        func.DatabaseData(msg=message, user=user_id).db_check_class()
        data = func.DatabaseData(msg=message, user=user_id).db_calc_avg_sum()
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Твоя текущая категория — _{data[0]}_\n\nТвой текущий средний чек:   *{data[1]} RUB*"
        )

    else:
        bot.send_message(message.chat.id, text="К сожалению я не смог распознать твою команду.")


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

        if call.message:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

            # алгоритм inline кнопок выбора категории при /start
            if value in ['cat_a', 'cat_b']:
                category = None
                if call.data.startswith('cat_a'):
                    category = buttons.class_a
                elif call.data.startswith('cat_b'):
                    category = buttons.class_b
                func.DatabaseData(msg=call.message, user=user_id, cls=category).db_update_class()
                return None

            # алгоритм inline кнопок внутри "Посмотреть ЗП"
            elif value in func.month_dict.keys():
                total_salary = func.DatabaseData(msg=call.message, user=user_id, month=value).db_get_total_sum()

                if total_salary is not None:
                    month = func.month_dict.get(value, {})
                    bot.send_message(chat_id=call.message.chat.id,
                                     text=f"Цифры за *{month.upper()}:*\n\n"
                                          f"*⚡ Первичка:*        {total_salary[0][0]}\n"
                                          f"*⚡ Гарант:*        {total_salary[0][1]}\n"
                                          f"*⚡ Холод:*     {total_salary[0][2]}\n"
                                          f"*⚡ Артём:*     {total_salary[0][3]}\n"
                                          f"*⚡ Чистые:*        {total_salary[0][4]}\n"
                                          f"*⚡ Непрофиль:*     {total_salary[0][5]}\n\n"
                                          f"*ИТОГО:*     {total_salary[1]} RUB")
                else:
                    bot.send_message(chat_id=call.message.chat.id, text="💾 Нет данных")
                return None

            # добавляет выбранную пользователем inline кнопку в БД из "Добавить приход"
            selected_button = None
            bot.send_message(chat_id=call.message.chat.id, text="Введи сумму 👇")

            if value == buttons.pervichka:
                selected_button = buttons.pervichka
            elif value == buttons.garant:
                selected_button = buttons.garant
            elif value == buttons.holod:
                selected_button = buttons.holod
            elif value == buttons.artem:
                selected_button = buttons.artem
            elif value == buttons.clean_money:
                selected_button = buttons.clean_money
            elif value == buttons.non_profile:
                selected_button = buttons.non_profile

            func.DatabaseData(msg=call.message, btn=selected_button, user=user_id).db_update_button()
            bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

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
