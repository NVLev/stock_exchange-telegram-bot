from loader import bot
from states.custom_states import Menu_states
from telebot.types import Message
from keyboards.reply.tiсkers import div_menu
from api.api_requests import tickers_list

@bot.message_handler(commands=['dividends'])
def dividends(message: Message) -> None:
    bot.set_state(message.from_user.id, Menu_states.dividends, message.chat.id)
    bot.send_message(message.from_user.id,
                     'Чтобы узнать дивиденды по акции за последные 4 года, введите тикер '
                     'или выберите из тикеров в меню', reply_markup=div_menu())

@bot.message_handler(content_types=['text'])
def handler(message: Message) -> None:
    if message.text == "Дивиденды по акции":
        bot.set_state(message.from_user.id, Menu_states.dividends, message.chat.id)
        bot.send_message(message.from_user.id,
                         'Чтобы узнать дивиденды по акции за последные годы, введите тикер '
                         'или выберите из тикеров в меню', reply_markup=div_menu())


@bot.message_handler(state=Menu_states.dividends)
def dividends_handler(message: Message) -> None:
    if message.text.upper() not in tickers_list:
        bot.send_message(message.from_user.id,
                         "Такого тикера нет в списке акций, посмотрите текущий список:"
                         ""
                        )