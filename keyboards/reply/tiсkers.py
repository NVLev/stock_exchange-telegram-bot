from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def div_menu() -> ReplyKeyboardMarkup:
    div_markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    sberkey = types.KeyboardButton('SBER')
    gazpkey = types.KeyboardButton('GAZP')
    tcsgkey = types.KeyboardButton('TCSG')
    lsrgkey = types.KeyboardButton('LSRG')
    tatnkey = types.KeyboardButton('TATNP')
    lukoilkey = types.KeyboardButton('LKOH')

    div_markup.add(sberkey, gazpkey, tcsgkey, lsrgkey, tatnkey, lukoilkey)
    return div_markup
