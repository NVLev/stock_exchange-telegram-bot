import api.api_requests
from loader import bot
from states.custom_states import Menu_states
from telebot.types import Message
from keyboards.reply.tiсkers import div_menu
import pandas as pd
import codecs
import csv
from tabulate import tabulate
from config_data.config import logger
import os

#  переписать хэндлер.
#  Он считает, что сообщение отправлено немедленно после получения статуса.
#  Может быть, написать пустой декоратор (которые с лямбдой), и в нем ставить условия.
#  Через reply (?)


def from_csv_to_list():
    with codecs.open(os.path.dirname(os.path.abspath(__file__))
          + "\\tickers.csv", "r", "utf-8") as file:
        reader = sum(list(csv.reader(file, skipinitialspace=True)), [])
    return reader
# message.from_user.id, KeyboardsState.buttons_count, message.chat.id
from_csv_to_list()
@bot.message_handler(commands=['dividends'])
def div_handler(message: Message) -> None:
    bot.set_state(message.from_user.id, Menu_states.waiting_for_ticker, message.chat.id)
    bot.send_message(message.from_user.id,
                     'Чтобы узнать дивиденды по акции за последные 4 года, введите тикер '
                     'или выберите из тикеров в меню', reply_markup=div_menu())


@bot.message_handler(content_types=['text'])
def handler(message: Message) -> None:
    if message.text == "Дивиденды по акции":
        logger.info("User %s запросил дивиденды")
        msg = bot.send_message(message.from_user.id,
                         'Чтобы узнать дивиденды по акции за последные годы, введите тикер '
                         'или выберите из тикеров в меню', reply_markup=div_menu())
        bot.set_state(message.from_user.id, Menu_states.waiting_for_ticker, message.chat.id)
        bot.register_next_step_handler(msg, dividend_handler)


def dividend_handler(message: Message) -> None:
    chat_id = message.chat.id
    current_state = bot.get_state(message.from_user.id, chat_id)
    if current_state == 'Menu_states:waiting_for_ticker':
        logger.info("проверено - waiting_for_ticker")
        ticker = message.text.upper()
        logger.info(ticker)
        tickers_list = from_csv_to_list()
        if ticker not in tickers_list:
            logger.info("введено сообщение")
            bot.send_message(message.from_user.id,
                             "Такого тикера нет в списке акций, посмотрите список:"
                             "\n https://www.moex.com/ru/listing/securities-list.aspx"
                             )
        else:
            answer = api.api_requests.dividends(ticker)
            df = pd.DataFrame(answer)
            bot.send_message(message.from_user.id, print(df))
        # Transition to a new state after processing the ticker
        # bot.set_state(message.from_user.id, Menu_states.dividend_result, message.chat.id)
    else:
        logger.info(bot.get_state(message.from_user.id, message.chat.id))
