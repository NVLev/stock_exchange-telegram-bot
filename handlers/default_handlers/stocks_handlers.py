
from api.api_requests import from_csv_to_list, instrument
from loader import bot
from telebot.types import Message
import reticker
from keyboards.inline.stocks_choices import stocks_choice
from keyboards.reply.default import main_menu
from keyboards.reply.stock_keyboard import stocks_menu
from config_data.config import logger
from states.custom_states import Menu_states

# user жмет акции - появляется меню - ввести тикер/выбрать/я не знаю тикер
# выбрать - меню (10-15 тикеров)
# поиск по названию - поработать с запросом

def stocks_handler1(message: Message) -> None:
    answer = message.text
    if answer == 'Знаю тикер':
        message_know = bot.send_message(message.from_user.id,
                               'Я весь внимание',
                               )
        bot.set_state(message.from_user.id, Menu_states.waiting_for_stocks_choice, message.chat.id)
        bot.register_next_step_handler(message_know, stocks_handler2)


def stocks_handler2(message: Message) -> None:
    """
    Обрабатывает ввод тикера для получения котировки
     - проверяет тикер по списку
     - если все в порядке, запускает функцию получения котировки
     - выводит информацию пользователю

    """
    chat_id = message.chat.id
    current_state = bot.get_state(message.from_user.id, chat_id)
    if current_state == 'Menu_states:waiting_for_stocks_choice':
        logger.info("проверено - waiting_for_stocks_choice")
        ticker = message.text.upper()
        logger.info(ticker)
        tickers_list = from_csv_to_list()
        if ticker not in tickers_list:
            logger.info("введено сообщение, акции нет в списке")
            bot.send_message(message.from_user.id,
                             "Такой акции я не знаю, посмотрите список:"
                             "\n https://www.moex.com/ru/listing/securities-list.aspx"
                             )
        else:
            logger.info("всё верно")
            try:
                df = instrument(ticker)
                table = df.to_string(columns=['secid', 'shortname', 'closeprice', 'settledate'],
                                     index=False, header=False, line_width=70,
                                     justify='left')
                bot.send_message(message.from_user.id, table)
                bot.send_message(message.from_user.id,
                                 'Хотите узнать ещё котировку или перейти в главное меню?',
                                 reply_markup=stocks_choice()
                                 )
            except Exception as e:
                bot.send_message(message.from_user.id,
                                 'Что-то пошло не так, вы перешли в главное меню',
                                 reply_markup=main_menu())
                return None
    else:
        logger.info(bot.get_state(message.from_user.id, message.chat.id))

@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == "more_stock"))
def answer_good(callback_query):
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    msg5 = bot.send_message(callback_query.from_user.id, 'OK')
    bot.register_next_step_handler(msg5, stocks_handler1)
    logger.info("ещё")
@bot.callback_query_handler(func=lambda callback_query: (
                callback_query.data == "cur_return"))
def answer_return(callback_query):
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    bot.send_message(callback_query.from_user.id,'Вы вернулись в главное меню',
                     reply_markup=main_menu())
    logger.info("возврат")