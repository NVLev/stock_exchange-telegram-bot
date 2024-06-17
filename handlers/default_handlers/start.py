from loader import bot
from states.custom_states import Menu_states
from telebot.types import Message
from keyboards.reply.default import menu

@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.send_message(message.chat.id, "Привет.  Я начинающий бот, могу кое-что спросить у Московской биржи. "
                          "Жми, чтобы узнать, что", reply_markup=menu())

