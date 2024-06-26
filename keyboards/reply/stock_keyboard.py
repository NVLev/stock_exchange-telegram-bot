from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def stocks_menu() -> ReplyKeyboardMarkup:
    rate_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    tick = types.KeyboardButton('Знаю тикер')
    choice = types.KeyboardButton('Хочу выбрать из того, что есть')
    not_know = types.KeyboardButton('Что-то хочу, но тикер не знаю')

    rate_markup.add(tick, choice, not_know)
    return rate_markup

def stock_ticker_menu() -> ReplyKeyboardMarkup:
    stock_ticker_markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    sberkey = types.KeyboardButton('SBER')
    gazpkey = types.KeyboardButton('GAZP')
    mtskey = types.KeyboardButton('ROSN')
    lsrgkey = types.KeyboardButton('SBERP')
    tatnkey = types.KeyboardButton('CHMF')
    lukoilkey = types.KeyboardButton('LKOH')
    surgutkey = types.KeyboardButton('SNGSP')
    banepkey = types.KeyboardButton('YNDX')
    nlmkkey = types.KeyboardButton('GMKN')
    mgntkey = types.KeyboardButton('MGNT')

    stock_ticker_markup.add(sberkey, gazpkey, mtskey, lsrgkey, tatnkey, lukoilkey, surgutkey, banepkey, nlmkkey, mgntkey)
    return stock_ticker_markup