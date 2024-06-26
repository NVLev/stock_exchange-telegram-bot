from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def div_menu() -> ReplyKeyboardMarkup:
    div_markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    sberkey = types.KeyboardButton('SBER')
    gazpkey = types.KeyboardButton('GAZP')
    mtskey = types.KeyboardButton('MTSS')
    lsrgkey = types.KeyboardButton('LSRG')
    tatnkey = types.KeyboardButton('TATNP')
    lukoilkey = types.KeyboardButton('LKOH')
    surgutkey = types.KeyboardButton('SNGSP')
    banepkey = types.KeyboardButton('BANEP')
    nlmkkey = types.KeyboardButton('NLMK')

    div_markup.add(sberkey, gazpkey, mtskey, lsrgkey, tatnkey, lukoilkey, surgutkey, banepkey, nlmkkey)
    return div_markup
