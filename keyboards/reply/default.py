from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def start_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton("Start")
    keyboard.add(KeyboardButton("Что я могу"))
    return keyboard

def main_menu() -> ReplyKeyboardMarkup:
    '''Создает Главное меню, которое появляется при нажатии start'''
    source_markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    source_markup_btn1 = types.KeyboardButton('Дивиденды по акции')
    source_markup_btn2 = types.KeyboardButton('Купоны по облигации')
    source_markup_btn3 = types.KeyboardButton('Цены акции за неделю')
    source_markup_btn4 = types.KeyboardButton('Подробнее')
    source_markup.add(source_markup_btn1, source_markup_btn2, source_markup_btn3, source_markup_btn4)
    return source_markup

