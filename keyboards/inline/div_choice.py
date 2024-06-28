from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def div_return() -> InlineKeyboardMarkup:
    div_answer = InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("💁 Ещё", callback_data='more')
    button2 = types.InlineKeyboardButton("🔙 Возвращаемся", callback_data='return')
    div_answer.add(button1, button2)
    return div_answer