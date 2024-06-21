from loader import bot
from states.custom_states import Menu_states
from telebot.types import Message
from keyboards.reply.default import main_menu
import logging
from config_data.config import logger



@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    logger.info("User %s started the conversation.")
    bot.send_message(message.chat.id, "Привет.  Я начинающий бот, могу кое-что спросить у Московской биржи. "
                          "Жми, чтобы узнать, что", reply_markup=main_menu())
    bot.set_state(message.from_user.id, Menu_states.start, message.chat.id)
