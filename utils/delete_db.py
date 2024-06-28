from telebot.types import Message
from database.chat_pewee import User
from loader import bot
from config_data.config import logger


@bot.message_handler(content_types=['left_chat_member'])
def handle_left_chat_member(message: Message) -> None:
    while True:
        try:
            query = User.delete()
            query.execute()
            logger.info('база стерта')
        except:
            logger.info('стереть не получилось')
            break