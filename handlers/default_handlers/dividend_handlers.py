import api.api_requests
from api.api_requests import from_csv_to_list
from . import stocks_handlers
from loader import bot
from states.custom_states import Menu_states
from telebot.types import Message
from keyboards.reply.default import main_menu
from keyboards.reply.tiсkers import div_menu
from keyboards.reply.rate import rate_menu
from keyboards.inline.div_choice import div_return
from keyboards.reply.stock_keyboard import stocks_menu
# from keyboards.inline.stocks_3choices import stocks_choice

import csv
from config_data.config import logger
import os
from . import currency_rate, stocks_handlers



from_csv_to_list()


@bot.message_handler(commands=['dividends'])
def div_handler(message: Message) -> None:
    """
    Обработка команды dividends
    на тот случай, если пользователь хочет вызвать
    информацию по дивидендам командой
    """
    bot.set_state(message.from_user.id, Menu_states.waiting_for_ticker, message.chat.id)
    bot.send_message(message.from_user.id,
                     'Чтобы узнать дивиденды по акции за последные 4 года, введите тикер '
                     'или выберите из тикеров в меню', reply_markup=div_menu())


@bot.message_handler(content_types=['text'])
def handler(message: Message) -> None:
    """Обрабатывает главное меню"""
    if message.text == "Дивиденды по акции":
        logger.info("User запросил дивиденды")
        msg = bot.send_message(message.from_user.id,
                               'Чтобы узнать дивиденды по акции за последные годы, введите тикер '
                               'или выберите из тикеров в меню', reply_markup=div_menu())
        bot.set_state(message.from_user.id, Menu_states.waiting_for_ticker, message.chat.id)
        bot.register_next_step_handler(msg, dividend_handler)
    elif message.text == 'Курсы валют':
        logger.info("User запросил курсы валют")
        msg2 = bot.send_message(message.from_user.id,
                               'Поскольку Московская биржа не проводит торги '
                               'по самым интересным валютам, я возьму курсы у ЦБ РФ. '
                               'Выбирай валюту, курс указан к рублю', reply_markup=rate_menu())
        bot.set_state(message.from_user.id, Menu_states.currency, message.chat.id)
        bot.register_next_step_handler(msg2, currency_rate.currency_handler)
    elif message.text == 'Котировка акции':
        logger.info("User запросил курс акций")
        msg4 = bot.send_message(message.from_user.id,
                               'Можете ввести тикер, выбрать из меню, '
                               'попытаться найти тикер по названию',
                                reply_markup=stocks_menu())
        bot.register_next_step_handler(msg4, stocks_handlers.stocks_handler1)
    elif message.text == 'Подробнее':
        logger.info("User запросил информацию")
        bot.send_message(message.from_user.id,
                         '"Дивиденды по акциям" - покажу все дивиденды, которые'
                         'выплачивала компания последние несколько лет (от 5 до 10, '
                         'если выплачивала, конечно), а также предстоящие дивиденды '
                         'в этом году, если по ним принято решение'
                         'в формате - ТИКЕР - дата - сумма.  Для получения информации'
                         'надо ввести тикер, но 9 тикеров я для вас уже приготовил.'
                         'Лайфхак - если не знаете тикер, можно попробовать его найти'
                         'в разделе "Котировка акций", выбрав соответствующую команду'
                         '"Курсы валют" - здесь всё просто, 8 валют, информация '
                         'представлена в виде id валюты - наименование - курс в рублях'
                         '"Котировка акций" - можно ввести тикер, выбрать из 10'
                         'самых популярных акций или поискать тикер по названию.')


def dividend_handler(message: Message) -> None:
    """
    Обрабатывает ввод тикера для получения котировок по акции
     - проверяет тикер по списку
     - если все в порядке, запускает функцию получения котировки
     - выводит информацию пользователю
    """
    chat_id = message.chat.id
    current_state = bot.get_state(message.from_user.id, chat_id)
    if current_state == 'Menu_states:waiting_for_ticker':
        logger.info("проверено - waiting_for_ticker")
        ticker = message.text.upper()
        logger.info(ticker)
        tickers_list = from_csv_to_list()
        if ticker not in tickers_list:
            logger.info("введено сообщение, тикера нет в списке")
            bot.send_message(message.from_user.id,
                             "Такого тикера нет в списке акций, посмотрите список:"
                             "\n https://www.moex.com/ru/listing/securities-list.aspx"
                             )
            bot.send_message(message.from_user.id,
                             'Хотите ввести ещё один токен или перейти в меню?',
                             reply_markup=div_return()
                             )
        else:
            logger.info("введено сообщение", ticker)
            try:
                df = api.api_requests.dividends(ticker)
                table = df.to_string(columns=['secid', 'registryclosedate', 'value', 'currencyid'],
                                     index=False, header=False, line_width=70,
                                     justify='left')
                bot.send_message(message.from_user.id, table)
                bot.send_message(message.from_user.id,
                                 'Хотите ввести ещё один токен или перейти в меню?',
                                 reply_markup=div_return()
                                 )
            except Exception as e:
                bot.send_message(message.from_user.id,
                                 'Что-то пошло не так, вы перешли в главное меню',
                                 reply_markup=main_menu())
                return None
        # bot.set_state(message.from_user.id, Menu_states.dividend_result, message.chat.id)
    else:
        logger.info(bot.get_state(message.from_user.id, message.chat.id))


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == "more"))
def answer_good(callback_query):
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    msg1 = bot.send_message(callback_query.from_user.id, 'OK')
    bot.register_next_step_handler(msg1, dividend_handler)
    logger.info("ещё")
@bot.callback_query_handler(func=lambda callback_query: (
                callback_query.data == "return"))
def answer_return(callback_query):
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    bot.send_message(callback_query.from_user.id,'Вы вернулись в главное меню',
                     reply_markup=main_menu())
    logger.info("возврат")
    # bot.set_state(message.from_user.id, Menu_states.start, message.chat.id))
