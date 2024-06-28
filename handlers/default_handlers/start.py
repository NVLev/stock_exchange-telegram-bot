from telebot.types import Message

from config_data.config import logger
from database.chat_pewee import User, create_models
from keyboards.reply.default import main_menu
from loader import bot
from states.custom_states import Menu_states


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    username = message.from_user.username
    logger.info("User started the conversation.")
    create_models()
    User.create(
        user_id=message.from_user.id,
        username=username,
        msg=message.text
    )
    bot.reply_to(message, "Привет.  Я начинающий бот, могу кое-что спросить у Московской биржи. "
                          "Жми, чтобы узнать", reply_markup=main_menu())
    bot.set_state(message.from_user.id, Menu_states.start, message.chat.id)
