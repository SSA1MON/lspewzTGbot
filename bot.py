import sqlite3
import telebot.types
import buttons
import func

from telebot import types, TeleBot
from config import TOKEN
from time import sleep

bot = TeleBot(token=TOKEN, parse_mode='Markdown')
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    """
    Функция обработчик. Обрабатывает команду /start
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton(buttons.add_cash)
    btn2 = types.KeyboardButton(buttons.check_salary)
    markup.add(btn1, btn2)

    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Перезапуск бота")
    ])

    # создает таблицу в бд, если её нет
    func.DatabaseData(msg=message, user=message.from_user.id).db_month_column()

    bot.send_message(message.chat.id,
                     text=f"Wassup, <b>{message.from_user.first_name}</b>!\n",
                     reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types=['text'])
def main(message: telebot.types.Message, msg: str = None) -> None:
    """
    Функция обработчик. Обрабатывает команды от кнопок в меню, при начале диалога с ботом (/start)
    """

    user_id = message.from_user.id
    if message.text == buttons.add_cash or msg == buttons.add_cash:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("Первичка", callback_data=f'{buttons.pervichka}|{user_id}')
        button2 = types.InlineKeyboardButton("Гарантия", callback_data=f'{buttons.garant}|{user_id}')
        button3 = types.InlineKeyboardButton("Холод", callback_data=f'{buttons.holod}|{user_id}')
        button4 = types.InlineKeyboardButton("Артём", callback_data=f'{buttons.artem}|{user_id}')
        button5 = types.InlineKeyboardButton("Чистые деньги", callback_data=f'{buttons.clean_money}|{user_id}')
        button6 = types.InlineKeyboardButton("Непрофиль", callback_data=f'{buttons.non_profile}|{user_id}')
        markup.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(chat_id=message.chat.id, text="Выбери нужную категорию:", reply_markup=markup)

    elif message.text == buttons.check_salary or msg == buttons.check_salary:
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

    else:
        bot.send_message(message.chat.id, text=f"К сожалению я не смог распознать твою команду.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery) -> None:
    """
    Функция обработчик. Обрабатывает запросы от кнопок из функции main().
    """
    try:
        user_id = call.data.split('|')[1]
        if call.message:
            if call.data.startswith(buttons.pervichka):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn=buttons.pervichka, user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith(buttons.garant):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn=buttons.garant, user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith(buttons.holod):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn=buttons.holod, user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith(buttons.artem):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn=buttons.artem, user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith(buttons.clean_money):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn=buttons.clean_money, user=user_id).db_update_button()
                bot.send_message(chat_id=call.message.chat.id, text="Введи сумму:")
                bot.register_next_step_handler(message=call.message, callback=func.answer_handler)

            elif call.data.startswith(buttons.non_profile):
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                func.DatabaseData(msg=call.message, btn=buttons.non_profile, user=user_id).db_update_button()
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
                    month = func.month_dict.get(call.data.split('|')[0], {}).upper()
                    bot.send_message(chat_id=call.message.chat.id,
                                     text=f"Цифры за <b>{month}:</b>\n\n"
                                          f"<b>⚡ Первичка:</b>      {total_salary[0][0]}\n"
                                          f"<b>⚡ Гарант:</b>        {total_salary[0][1]}\n"
                                          f"<b>⚡ Холод:</b>     {total_salary[0][2]}\n"
                                          f"<b>⚡ Артём:</b>     {total_salary[0][3]}\n"
                                          f"<b>⚡ Чистые:</b>        {total_salary[0][4]}\n"
                                          f"<b>⚡ Непрофиль:</b>     {total_salary[0][5]}\n\n"
                                          f"<b>ИТОГО:</b>     {total_salary[1]} RUB",
                                     parse_mode='html')
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
