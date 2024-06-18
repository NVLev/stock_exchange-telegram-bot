import telebot
from telebot import types
import requests
import sqlite3
import pandas as pd
from tabulate import tabulate

from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    """
    Обрабатывает команду /start, создает базу данный, выводит приветствие и обращается к функции главного меню
    """
    db = sqlite3.connect('moex_bot.sql')
    cur = db.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS portfolio (id int, code text, stock text, number int, quote int, value int)
    """
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()

    mess = (
        f'Привет, {message.from_user.first_name}! Я бот - помощник инвестора, умею выводить состав и текущую стоимость '
        f'Вашего потрефеля акций на Московской Бирже. В первую очередь буду полезен, если у Вас портфель '
        f'разбросан по разным брокерам, помогу отображать его общий состав и стоимость')
    bot.send_message(message.chat.id, mess)
    main_menu(message)

def main_menu(message):
    """
    Создает и выывдит главное меню
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    show_portfolio = types.KeyboardButton('Состав и стоимость портфеля')
    change_portfolio = types.KeyboardButton('Изменить портфель')
    markup.add(show_portfolio, change_portfolio)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    bot.register_next_step_handler(message, menu_text)

@bot.message_handler(content_types=["text"])
def menu_text(message):
    """
    Обрабатывает кнопки (сообщения) главного меню
    """
    global quotes_csv_text
    if message.text == 'Состав и стоимость портфеля':
        url = "https://iss.moex.com/iss/engines/stock/markets/" \
            "shares/boards/TQBR/securities.csv?iss.meta=off&iss." \
            "only=marketdata&marketdata.columns=SECID,LAST"
        quotes_csv_text = requests.get(url).text.split('\n')
        id = message.chat.id
        db = sqlite3.connect('moex_bot.sql')
        cur = db.cursor()

        if len(quotes_csv_text[2].split(';')[1]) == 0:
            bot.send_message(message.chat.id, f'{message.from_user.first_name}, извините, нет доступа '
                                                    f'к серверу биржи, котировки и стоимость сейчас показать не согу, '
                                                    f'поробуйте, пожалуйста, позже')

            sql = """
            SELECT code, stock, number FROM portfolio WHERE id = ?
            """
            table = cur.execute(sql, (id,))
#            header_rus = ['Код', 'Акция', 'Кол-во']
#            text = tabulate(table, tablefmt='plain', headers=header_rus, stralign=alignments)
#            table = tabulate(values, headers="firstrow", tablefmt="simple", stralign=alignments)
            text = 'Код       Кол-во \n'
            for i in cur.fetchall():
                text += i[0].ljust(13 - len(str(i[0]))) + \
                    str(i[2]).ljust(17 - len(str(i[2]))) + '\n'

            bot.send_message(message.chat.id, text)
        else:
            sql = """
            SELECT * FROM portfolio WHERE id = ?
            """
            cur.execute(sql, (id,))
            for i in cur.fetchall():
                sql = """
                UPDATE portfolio SET quote = ?, value = ? WHERE id = ? AND code = ?
                """
                cur.execute(sql, (last_price_stock(i[1]), round(last_price_stock(i[1]) * i[3], 2), i[0], i[1]))
                db.commit()
#            sql = """
#            SELECT code, stock, number, quote, value FROM portfolio WHERE id = ? ORDER BY value DESC
#            """
#            cur.execute(sql, (id,))
#            table = cur.fetchall()
#            header_rus = ['Код', 'Акция', 'Кол-во', 'Кот-ка', 'Ст-сть']
#            text = tabulate(table, tablefmt='plain', headers=header_rus)
#            alignments = ['code', 'stock', 'number', 'quote', 'value'] * 5
#            text = tabulate(table, tablefmt='plain', headers=header_rus, stralign=alignments)
#            bot.send_message(message.chat.id, text)

            text = 'Код       Кол-во       Котировка     Стоимость\n'
            db = sqlite3.connect('moex_bot.sql')
            cur = db.cursor()
            sql = """
            SELECT * FROM portfolio WHERE id = ? ORDER BY code
            """
            cur.execute(sql, (id,))
            for i in cur.fetchall():
                text += i[1].ljust(13 - len(str(i[1]))) + \
                    str(i[3]).ljust(17 - len(str(i[3]))) + \
                    str(i[4]).ljust(26 - len(str(i[4]))) + \
                    str(i[5]).ljust(40 - len(str(i[5]))) + '\n'
            bot.send_message(message.chat.id, text)

            sql = """
            SELECT SUM(value) FROM portfolio WHERE id = ?
            """
            cur.execute(sql, (id,))
            total = cur.fetchall()
            text = f'Общая стоимость портфеля: {round(total[0][0], 2)} руб'
            bot.send_message(message.chat.id, text)
        cur.close()
        db.close()
        main_menu(message)
    elif message.text == 'Изменить портфель':
        change_portfolio(message)

def last_price_stock(code):
    """
    Принимает на вход код акции, находит в цикле соответсвующиую котировку и возвращает ее
    """
    for quotes_csv_line in quotes_csv_text:
        quotes_csv_tabl = quotes_csv_line.split(';')
        if quotes_csv_tabl[0] == code:
            return float(quotes_csv_tabl[1])

def change_portfolio(message):
    """
    Выводит меню "изменить портфель"
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    add_to_portfolio = types.KeyboardButton('Куплены акции, добваить в портфель')
    delete_from_portfolio = types.KeyboardButton('Проданы акции, удалить из портфеля')
    delete_portfolio = types.KeyboardButton('Удалить портфель')
    back = types.KeyboardButton('Назад')
    markup.add(add_to_portfolio, delete_from_portfolio, delete_portfolio, back)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    bot.register_next_step_handler(message, change_portfolio_text)

@bot.message_handler(content_types=["text"])
def change_portfolio_text(message):
    """
    Обрабатывает кнопки (сообщения) меню 'Изменить портфель'
    """
    if message.text == 'Куплены акции, добваить в портфель':
        bot.send_message(message.chat.id, 'Введите через пробел код акции и купленное количество, например: SBER 200')
        bot.register_next_step_handler(message, stock_buy_add)
    elif message.text == 'Проданы акции, удалить из портфеля':
        bot.send_message(message.chat.id, 'Введите через пробел код акции и проданное количество, например: GAZP 150')
        bot.register_next_step_handler(message, stock_sell_delete)
    elif message.text == 'Удалить портфель':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        yes_delete = types.KeyboardButton('Да, удалить')
        no_back = types.KeyboardButton('Нет, назад')
        markup.add(yes_delete, no_back)
        text = 'Вы точно хотите удалить портфель? Это действие необратимо'
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, delete_portfolio_text)
    elif message.text == 'Назад':
        main_menu(message)

def stock_buy_add(message):
    """
    Принимает на вход сообщение, отправленное полсе "Купил акции", проверяет сообщение на ошибки воода
    и добавляет акции в портфель (БД)
    """
    stock_code = pd.read_excel("stock_code.xlsx")

    id = message.chat.id
    code = message.text.strip().split(' ')[0].upper()

    if len(message.text.strip().split(' ')) != 2:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, нужно ввести два значения, '
                                                f'код и количество, пожалуйста, попробуйте еще раз')
    elif stock_code[stock_code['code'] == code].shape[0] == 0:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, такого кода акции не существует, '
                                                f'пожалуйста, попробуйте еще раз')
    else:
        try:
            number = int(message.text.strip().split(' ')[1])
            stock = stock_code[stock_code['code'] == code]['stock'].to_string(index=False)
            db = sqlite3.connect('moex_bot.sql')
            cur = db.cursor()
            sql = """
            SELECT code FROM portfolio WHERE id = ? AND code = ?
            """
            cur.execute(sql, (id, code))

            if len(cur.fetchall()) == 0:
                sql = """
                INSERT INTO portfolio VALUES (?, ?, ?, ?, 0, 0)
                """
                cur.execute(sql, (id, code, stock, number))
                db.commit()
            else:
                sql = """
                SELECT number FROM portfolio WHERE id = ? AND code = ?
                """
                cur.execute(sql, (id, code))
                number_new = number + cur.fetchall()[0][0]
                sql = """
                UPDATE portfolio SET number = ? WHERE id = ? AND code = ?
                """
                cur.execute(sql, (number_new, id, code))
                db.commit()

            db.commit()
            cur.close()
            db.close()

            bot.send_message(message.chat.id, f'{number} акций {stock} добавлены в портфель!')
        except:
            bot.send_message(message.chat.id, f'{message.from_user.first_name}, вторым значением должно '
                                                    f'быть число акций, пожалуйста, попробуйте еще раз')
    change_portfolio(message)

def stock_sell_delete(message):
    """
    Принимает на вход сообщение, отправленное полсе "Продал акции", проверяет сообщение на ошибки воода
    и удаляет акции из портфеля (БД)
    """
    stock_code = pd.read_excel("stock_code.xlsx")
    code = message.text.strip().split(' ')[0].upper()
    if len(message.text.strip().split(' ')) != 2:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, нужно ввести два значения, код и '
                                                f'количество, пожалуйста, попробуйте еще раз')
    elif stock_code[stock_code['code'] == code].shape[0] == 0:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, такого кода акции не существует, '
                                                f' пожалуйста, попробуйте еще раз')
    else:
        try:
            number = int(message.text.strip().split(' ')[1])
            stock = stock_code[stock_code['code'] == code]['stock'].to_string(index=False)
            id = message.chat.id

            db = sqlite3.connect('moex_bot.sql')
            cur = db.cursor()
            sql = """
            SELECT code FROM portfolio WHERE id = ? AND code = ?
            """
            cur.execute(sql, (id, code))

            if len(cur.fetchall()) == 0:
                bot.send_message(message.chat.id, f'{message.from_user.first_name}, таких акций нет в Вашем '
                                                  f'портфеле, пожалуйста, попробуйте еще раз')
            else:
                sql = """
                SELECT number FROM portfolio WHERE id = ? AND code = ?
                """
                cur.execute(sql, (id, code))
                number_old = cur.fetchall()[0][0]
                if number_old < number:
                    bot.send_message(message.chat.id, f'{message.from_user.first_name}, количество проданных акций '
                                                      f'больше, чем есть в Вашем портфеле '
                                                      f', пожалуйста, попробуйте еще раз')
                elif number_old == number:
                    sql = """
                    DELETE FROM portfolio WHERE id = ? AND code = ?
                    """
                    cur.execute(sql, (id, code))
                    bot.send_message(message.chat.id, f'{number} акций {stock} удалены из портфеля!')
                else:
                    number_new = number_old - number
                    sql = """
                    UPDATE portfolio SET number = ? WHERE id = ? AND code = ?
                    """
                    cur.execute(sql, (number_new, id, code))
                    bot.send_message(message.chat.id, f'{number} акций {stock} удалены из портфеля!')

            db.commit()
            cur.close()
            db.close()
        except:
            bot.send_message(message.chat.id, f'{message.from_user.first_name}, вторым значением должно быть число '
                                                    f'акций, пожалуйста, попробуйте еще раз')
    change_portfolio(message)

@bot.message_handler(content_types=["text"])
def delete_portfolio_text(message):
    """
    Обрабатывает кнопки (сообщения) меню 'Удалить портфель'
    """
    if message.text == 'Да, удалить':
        id = message.chat.id
        db = sqlite3.connect('moex_bot.sql')
        cur = db.cursor()
        sql = """
        DELETE FROM portfolio WHERE id = ?
        """
        cur.execute(sql, (id,))
        db.commit()
        cur.close()
        db.close()
        bot.send_message(message.chat.id, 'Ваш портфель полностью удален')
#    elif message.text == 'Нет, назад':
#        pass
    change_portfolio(message)

bot.polling(none_stop=True)