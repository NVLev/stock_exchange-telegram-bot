from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def stocks_menu() -> ReplyKeyboardMarkup:
    rate_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    tick = types.KeyboardButton('Знаю тикер')
    choice = types.KeyboardButton('Хочу выбрать из того, что есть')
    not_know = types.KeyboardButton('Что-то хочу, но тикер не знаю')

    rate_markup.add(tick, choice, not_know)
    return rate_markup