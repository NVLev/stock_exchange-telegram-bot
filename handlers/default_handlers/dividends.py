from loader import bot
from states.custom_states import Menu_states
from telebot.types import Message
from keyboards.reply.tiсkers import div_menu
# from api.api_requests import tickers_list
from api.api_requests import query, dividends, from_csv_to_list


# message.from_user.id, KeyboardsState.buttons_count, message.chat.id

@bot.message_handler(commands=['dividends'])
def div_handler(message: Message) -> None:
    bot.set_state(message.from_user.id, Menu_states.waiting_for_ticker, message.chat.id)
    bot.send_message(message.from_user.id,
                     'Чтобы узнать дивиденды по акции за последные 4 года, введите тикер '
                     'или выберите из тикеров в меню', reply_markup=div_menu())


@bot.message_handler(content_types=['text'])
def handler(message: Message) -> None:
    if message.text == "Дивиденды по акции":
        bot.set_state(message.from_user.id, Menu_states.waiting_for_ticker, message.chat.id)
        bot.send_message(message.from_user.id,
                         'Чтобы узнать дивиденды по акции за последные годы, введите тикер '
                         'или выберите из тикеров в меню', reply_markup=div_menu())


@bot.message_handler(state=Menu_states.waiting_for_ticker)
def dividends_handler(message: Message) -> None:
    if bot.get_state(message.from_user.id, message.chat.id) == Menu_states.waiting_for_ticker:
        ticker = message.text.upper()
        tickers_list = from_csv_to_list("tickers.txt")
        if ticker not in tickers_list:
            bot.send_message(message.from_user.id,
                             "Такого тикера нет в списке акций, посмотрите список:"
                             "\n https://www.moex.com/ru/listing/securities-list.aspx"
                             )
        else:
            answer = dividends(ticker)
            bot.send_message(message.from_user.id, answer)
        # Transition to a new state after processing the ticker
        bot.set_state(message.from_user.id, Menu_states.dividend_result, message.chat.id)
