from telebot.types import Message
from database.chat_pewee import User
import api.cur_cbrf
from config_data.config import logger
from keyboards.inline.cur_choice import cur_return
from keyboards.reply.default import main_menu
from keyboards.reply.rate import rate_menu
from loader import bot
from states.custom_states import Menu_states


@bot.message_handler(commands=['currency'])
def menu_currency_handler(message: Message) -> None:
    """
    Обработчик команды currency
    на тот случай, если user хочет вызвать курс валют командой
    """
    logger.info("команда currency")
    User.create(
        user_id=message.from_user.id,
        username=message.from_user.username,
        msg=message.text
    )
    cur_msg = bot.send_message(message.from_user.id,
                               'Поскольку Московская биржа не проводит торги '
                               'по самым интересным валютам, я возьму курсы у ЦБ РФ. '
                               'Выбирай валюту, курс указан к рублю', reply_markup=rate_menu())
    bot.set_state(message.from_user.id, Menu_states.currency, message.chat.id)
    bot.register_next_step_handler(cur_msg, currency_handler)


def currency_handler(message: Message) -> None:
    """
    Обработчик меню Курс валют.
    Запускает функцию api.cur_cbrf.get_currency_rate с аргументом
    текста на кнопке
    """
    chat_id = message.chat.id
    current_state = bot.get_state(message.from_user.id, chat_id)
    if current_state == 'Menu_states:currency':
        logger.info("проверено - User хочет валюту))")
        cur_name = message.text
        User.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            msg=cur_name
        )
        logger.info(cur_name)
        df_cur = api.cur_cbrf.get_currency_rate(cur_name)
        logger.info(df_cur)
        if cur_name == 'Армянских драмов' or cur_name == 'Турецких лир':
            table = df_cur.to_string(columns=['CharCode', 'Nominal', 'Name', 'Value'],
                                     index=False, header=False, line_width=70,
                                     justify='left')
        else:
            table = df_cur.to_string(columns=['CharCode', 'Name', 'Value'],
                                     index=False, header=False, line_width=70,
                                     justify='left')
        bot.send_message(message.from_user.id, table)
        bot.send_message(message.from_user.id,
                         'Хотите узнать курс другой валюты или перейти в  Главное меню?',
                         reply_markup=cur_return()
                         )
    else:
        logger.info("что-то пошло не так", current_state)


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == "more_cur"))
def answer_more(callback_query):
    """
    Обработчик inline menu,
    предоставляет возможность пользователю ввести другую валюту
    """
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    msg3 = bot.send_message(callback_query.from_user.id, 'OK')
    bot.register_next_step_handler(msg3, currency_handler)
    logger.info("ещё")


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == "cur_return"))
def answer_return2(callback_query):
    """
        Обработчик inline menu,
        предоставляет возможность пользователю вернуться в главное меню
        """
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    bot.send_message(callback_query.from_user.id, 'Вы вернулись в главное меню',
                     reply_markup=main_menu())
    logger.info("возврат")
