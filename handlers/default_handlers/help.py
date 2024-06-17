from loader import bot
from states.custom_states import Menu_states
from telebot.types import Message
from keyboards.reply.tikers import div_menu

from config_data.config import DEFAULT_COMMANDS



@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))