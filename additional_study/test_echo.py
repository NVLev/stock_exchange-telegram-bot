import telebot
from config_data import config

bot = telebot.TeleBot(token=config.BOT_TOKEN)  # Токен, полученный от BotFather.

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hello world!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    bot.infinity_polling()