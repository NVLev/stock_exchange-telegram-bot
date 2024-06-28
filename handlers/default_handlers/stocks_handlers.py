from telebot.types import Message
from database.chat_pewee import User
import api.api_requests
from api.api_requests import from_csv_to_list
from config_data.config import logger
from keyboards.inline.stocks_choices import stocks_choice, after_search
from keyboards.reply.default import main_menu
from keyboards.reply.stock_keyboard import stock_ticker_menu, stocks_menu
from loader import bot
from states.custom_states import Menu_states


# user жмет акции - появляется меню - ввести тикер/выбрать/я не знаю тикер
# выбрать - меню (10-15 тикеров)
# поиск по названию - поработать с запросом + доп. инлайн меню (Теперь знаете тикер)
# доп. - поработать с empty dataframe
@bot.message_handler(commands=['stock'])
def div_handler(message: Message) -> None:
    """
    Обработка команды dividends
    на тот случай, если пользователь хочет вызвать
    информацию по дивидендам командой
    """
    logger.info("User запросил курс акций")
    User.create(
        user_id=message.from_user.id,
        username=message.from_user.username,
        msg=message.text
    )
    stock_msg = bot.send_message(message.from_user.id,
                                 'Можете ввести тикер, выбрать из меню, '
                                 'попытаться найти тикер по названию',
                                 reply_markup=stocks_menu())
    bot.register_next_step_handler(stock_msg, stocks_handler1)


def stocks_handler1(message: Message) -> None:
    logger.info("Юзер перешел в меню по акциям")
    answer = message.text
    if answer == 'Знаю тикер':
        message_know = bot.send_message(message.from_user.id,
                                        'Я весь внимание',
                                        )
        User.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            msg=message.text
        )
        bot.set_state(message.from_user.id, Menu_states.waiting_for_stocks_choice, message.chat.id)
        bot.register_next_step_handler(message_know, stocks_handler2)
    elif answer == 'Хочу выбрать из того, что есть':
        message_know = bot.send_message(message.from_user.id,
                                        'Я знаю котировки по 10 акциям из народного портфеля.  Выбирайте',
                                        reply_markup=stock_ticker_menu()
                                        )
        User.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            msg=message.text
        )
        bot.set_state(message.from_user.id, Menu_states.waiting_for_stocks_choice, message.chat.id)
        bot.register_next_step_handler(message_know, stocks_handler2)
    elif answer == 'Что-то хочу, но тикер не знаю':
        message_smth = bot.send_message(message.from_user.id,
                                        'Так-так... Ну попробуйте ввести часть названия'
                                        )
        User.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            msg=message.text
        )
        bot.set_state(message.from_user.id, Menu_states.waiting_for_stocks_choice,
                      message.chat.id)
        bot.register_next_step_handler(message_smth, stocks_handler3)


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
        User.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            msg=message.text
        )
        logger.info(ticker)
        tickers_list = from_csv_to_list()
        if ticker not in tickers_list:
            logger.info("введено сообщение, акции нет в списке")
            bot.send_message(message.from_user.id,
                             "Такой акции я не знаю, посмотрите список:"
                             "\n https://www.moex.com/ru/listing/securities-list.aspx"
                             )
            bot.send_message(message.from_user.id,
                             'Хотите узнать ещё котировку или перейти в главное меню?',
                             reply_markup=stocks_choice()
                             )
        else:
            logger.info("всё верно")
            try:
                df = api.api_requests.instrument(ticker)
                table = df.to_string(columns=['SECID', 'SHORTNAME', 'PREVLEGALCLOSEPRICE', 'SETTLEDATE'],
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


def stocks_handler3(message: Message) -> None:
    chat_id = message.chat.id
    current_state = bot.get_state(message.from_user.id, chat_id)
    if current_state == 'Menu_states:waiting_for_stocks_choice':
        logger.info("проверено - waiting_for_stocks_choice")
        smth = message.text.lower()
        User.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            msg=message.text
        )
        logger.info(smth)
        try:
            df = api.api_requests.stocks_list(smth)
            table = df.to_string(columns=['secid', 'name'],
                                 index=False, header=False, line_width=80,
                                 justify='center')
            bot.send_message(message.from_user.id, table)
            bot.send_message(message.from_user.id,
                             'Теперь вы знаете тикер?',
                             reply_markup=after_search()
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
    msg5 = bot.send_message(callback_query.from_user.id, 'OK', reply_markup=stocks_menu())
    bot.register_next_step_handler(msg5, stocks_handler1)
    logger.info("ещё")


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == 'stock_return'))
def answer_return(callback_query):
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    bot.send_message(callback_query.from_user.id, 'Вы вернулись в главное меню',
                     reply_markup=main_menu())
    logger.info("возврат")


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == "yes"))
def answer_yes(callback_query):
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    y_msg = bot.send_message(callback_query.from_user.id, 'Прекрасно, возвращаю меню акций',
                             reply_markup=stocks_menu())
    bot.register_next_step_handler(y_msg, stocks_handler1)
    logger.info("получилось")


@bot.callback_query_handler(func=lambda callback_query: (
        callback_query.data == 'no'))
def answer_no(callback_query):
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    no_msg = bot.send_message(callback_query.from_user.id, 'Можно попробовать ещё',
                              reply_markup=stocks_menu())
    bot.register_next_step_handler(no_msg, stocks_handler1)
    logger.info("получилось")
