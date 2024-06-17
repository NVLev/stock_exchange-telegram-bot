from loader import bot
from states.custom_states import Menu_states
from telebot.types import Message
from keyboards.reply.tikers import div_menu


@bot.message_handler(commands=['dividends'])
def dividends(message: Message) -> None:
    bot.set_state(message.from_user.id, Menu_states.dividends, message.chat.id)
    bot.send_message(message.from_user.id,
                     'Чтобы узнать дивиденды по акции за последные 4 года, введите тикер '
                     'или выберите из тикеров в меню', reply_markup=div_menu())

@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == "Дивиденды по акции":
        bot.set_state(message.from_user.id, Menu_states.dividends, message.chat.id)
        bot.send_message(message.from_user.id,
                         'Чтобы узнать дивиденды по акции за последные 4 года, введите тикер '
                         'или выберите из тикеров в меню', reply_markup=div_menu())

