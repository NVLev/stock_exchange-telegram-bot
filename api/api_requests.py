from config_data.config import API_BASE_URL
import pandas as pd
from config_data.config import logger
# import json
import codecs
import os
import csv
from tabulate import tabulate
import requests
from urllib import parse


def from_csv_to_list():
    """Функция для проверки наличия тикера в базе"""
    with codecs.open(os.path.dirname(os.path.abspath(__file__))
                     + "\\tickers.csv", "r", "utf-8") as file:
        reader = sum(list(csv.reader(file, skipinitialspace=True)), [])
    return reader

pd.set_option("display.max_columns", 15)




def query(method: str, **kwargs) -> dict:
    """
    Функция для отправки запроса к ISS MOEX
    :param method:
    :param kwargs:
    :return:
    """
    try:
        url = API_BASE_URL % method
        if kwargs: url += "?" + parse.urlencode(kwargs)
        response = requests.get(url)
        response.encoding = 'utf-8'
        response_dict = response.json()
        return response_dict

    except Exception as e:
        print("query error %s" % str(e))
        return None


def flatten(response_dict: dict, blockname: str) -> list:
    """
    Функция для получения двумерного массива (словаря)
    :param response_dict:
    :param blockname:
    :return:
    """
    return [{k: r[i] for i, k in enumerate(response_dict[blockname]['columns'])}
            for r in response_dict[blockname]['data']]


# "https://iss.moex.com/iss/%s.json"
# def stock_list():
#     # Список бумаг торгуемых на московской бирже
#     r_list = query("securities", group_by="type", group_by_filter="common_share",
#                    limit=60)
#     flat = flatten(r_list, 'securities')
#     print(pd.DataFrame(flat, columns=['secid', 'shortname']))


def dividends(secid):
    method = "securities/%s/dividends" % secid
    j = query(method)
    flat = flatten(j, 'dividends')
    # print(pd.DataFrame(flat, columns=['secid', 'registryclosedate', 'value', 'currencyid']))
    # print(flat)
    return pd.DataFrame(flat, columns=['secid', 'registryclosedate', 'value', 'currencyid'])
    # return (pd.DataFrame(flat))
    # print(pd.DataFrame(f, columns=['secid','shortname' ,'primary_boardid', 'type']))
    # print(json.dumps(j, ensure_ascii=False, indent=4, sort_keys=True)


def instrument(secid: str) -> pd.DataFrame:
    method = 'engines/stock/markets/shares/boards/TQBR/securities/%s' % secid
    j = query(method)
    logger.info('пройдено - query')
    flat = flatten(j, 'securities')
    return pd.DataFrame(flat, columns=['SECID', 'SHORTNAME', 'PREVLEGALCLOSEPRICE', 'SETTLEDATE'])
        #pd.DataFrame(flat, columns=['secid', 'shortname', 'closeprice', 'settledate']))

def stocks_list(name: str) -> pd.DataFrame:
    """Список бумаг торгуемых на московской бирже"""
    # https://iss.moex.com/iss/reference/5
    j = query("securities", q=name, group_by="group", group_by_filter='stock_shares', limit=5
              )
    flat = flatten(j, 'securities')
    short_list = []
    for stock in flat:
        if len(stock['secid']) == 4 or len(stock['secid']) == 5:
            short_list.append(stock)
    return pd.DataFrame(short_list, columns=['secid', 'name'])

# if __name__ == '__main__':
#         df = stocks_list('сбер')
#         # print(df)
#         table = df.to_string(columns=['secid', 'name'],
#                              index=False, header=False, line_width=70,
#                              justify='left')
#         print(table)

