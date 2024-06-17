import telebot # telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States

# States storage
from telebot.storage import StateMemoryStorage

# Не забыть импортировать в __init__


state_storage = StateMemoryStorage()

class Menu_states(StatesGroup):
    dividends = State()
    currency = State()
    stock = State()


