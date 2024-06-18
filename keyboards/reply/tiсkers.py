from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def div_menu()-> ReplyKeyboardMarkup:
        div_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        sberkey = types.KeyboardButton('/stock SBER')
        gazpkey = types.KeyboardButton('/stock GAZP')
        tcsgkey = types.KeyboardButton('/stock TCSG')
        exitkey = types.KeyboardButton('/exit')
        div_markup.add(sberkey, gazpkey, tcsgkey, exitkey)
        return div_markup