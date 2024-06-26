from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def stocks_choice() -> InlineKeyboardMarkup:
    stocks_choice = InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("😎 Ещё", callback_data="more_stock")
    button2 = types.InlineKeyboardButton("Возвращаемся", callback_data='stock_return')
    stocks_choice.add(button1, button2)
    return stocks_choice