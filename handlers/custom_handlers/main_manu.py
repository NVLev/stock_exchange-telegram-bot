from loader import bot
from dividends import dividends
@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == "Дивиденды по акции":
        dividends()
    if message.text == "Как дела?":
        bot.send_message(message.chat.id, "Отлично!")