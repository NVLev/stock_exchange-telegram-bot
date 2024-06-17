from telebot.types import Message
from keyboards.reply.default import menu
from loader import bot
from states.custom_states import Menu_states

@bot.message_handler(commands=["start", "exit"])
def bot_start(message: Message):
    bot.send_message(message.chat.id, "Привет.  Я начинающий бот, могу кое-что спросить у Московской биржи. "
                          "Жми, чтобы узнать, что", reply_markup=menu())
    if message.text == "Дивиденды по акции":
        bot.set_state(message.from_user.id, Menu_states.dividends, message.chat.id)
