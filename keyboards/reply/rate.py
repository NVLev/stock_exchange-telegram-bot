from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def rate_menu() -> ReplyKeyboardMarkup:
    rate_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    gbkey = types.KeyboardButton('Фунт стерлингов Соединенного королевства')
    eurkey = types.KeyboardButton('Евро')
    cnykey = types.KeyboardButton('Китайский юань')
    hkdkey = types.KeyboardButton('Гонконгский доллар')
    trykey = types.KeyboardButton('Турецких лир')
    bynkey = types.KeyboardButton('Белорусский рубль')
    bgnkey = types.KeyboardButton('Болгарский лев')
    amdkey = types.KeyboardButton('Армянских драмов')

    rate_markup.add(gbkey, eurkey, cnykey, hkdkey, trykey, bynkey, bgnkey, amdkey)
    return rate_markup