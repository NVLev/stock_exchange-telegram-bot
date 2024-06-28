from typing import List

from telebot.types import Message
from database.chat_pewee import User
from config_data.config import DEFAULT_COMMANDS
from config_data.config import logger
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    logger.info("User asked help")
    bot.reply_to(message, "\n".join(text))


@bot.message_handler(commands=['history'])
def get_history(message: Message) -> None:
    logger.info(User.select())
    for msgs in User.select():
        bot.send_message(message.from_user.id, msgs)
