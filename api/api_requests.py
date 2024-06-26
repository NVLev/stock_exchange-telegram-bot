from config_data.config import API_BASE_URL
import pandas as pd
# import json
import codecs
import os
import csv
from tabulate import tabulate
import requests
from urllib import parse


def from_csv_to_list():
    with codecs.open(os.path.dirname(os.path.abspath(__file__))
                     + "\\tickers.csv", "r", "utf-8") as file:
        reader = sum(list(csv.reader(file, skipinitialspace=True)), [])
    return reader

pd.set_option("display.max_columns", 15)




def query(method: str, **kwargs):
    """
    Отправляю запрос к ISS MOEX
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


def flatten(response_dict: dict, blockname: str):
    """
    Собираю двумерный массив (словарь)
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


def instrument(secid):
    method = 'engines/stock/markets/shares/boards/TQBR/securities/%s' % secid
    j = query(method)
    flat = flatten(j, 'securities')
    return pd.DataFrame(flat)
        #pd.DataFrame(flat, columns=['secid', 'shortname', 'closeprice', 'settledate']))


if __name__ == '__main__':
        df = instrument('SBER')
        print(df)
        table = df.to_string(columns=['secid', 'shortname', 'closeprice', 'settledate'],
                             index=False, header=False, line_width=70,
                             justify='left')
        print(table)
# # # # #     stock_list()
