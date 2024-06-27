from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def stocks_choice() -> InlineKeyboardMarkup:
    stocks_choice = InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("😎 Ещё", callback_data="more_stock")
    button2 = types.InlineKeyboardButton("Возвращаемся", callback_data='stock_return')
    stocks_choice.add(button1, button2)
    return stocks_choice

def after_search() -> InlineKeyboardMarkup:
    after_choice = InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Да, теперь я знаю тикер", callback_data="yes")
    button2 = types.InlineKeyboardButton("Нет, хочу попробовать ещё", callback_data='no')
    after_choice.add(button1, button2)
    return after_choice