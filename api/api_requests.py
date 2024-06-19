from config_data.config import API_BASE_URL
import pandas as pd
# import json
import csv
import codecs
import requests
from urllib import parse

pd.set_option("display.max_columns", 15)


def from_csv_to_list(file_name):
    with codecs.open(file_name, "r", "utf-8") as file:
        reader = sum(list(csv.reader(file, skipinitialspace=True)), [])
    return reader


# tickers_list = from_csv_to_list("tickers.txt")
# print(tickers_list)


# request_url = ('https://iss.moex.com/iss/engines/stock/'
#                'markets/shares/boards/TQBR/securities.json')
# arguments = {'securities.columns': ('SECID,'
#                                     'REGNUMBER,'
#                                     'LOTSIZE,'
#                                     'SHORTNAME')}
# with requests.Session() as session:
#     iss = apimoex.ISSClient(session, request_url, arguments)
#     data = iss.get()
#     df = pd.DataFrame(data['securities'])
#     df.set_index('SECID', inplace=True)
#     print(df.head(), '\n')
#     print(df.tail(), '\n')
#     df.info()

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
def stock_list():
    # Список бумаг торгуемых на московской бирже
    r_list = query("securities", group_by="type", group_by_filter="common_share",
                   limit=60)
    flat = flatten(r_list, 'securities')
    print(pd.DataFrame(flat, columns=['secid', 'shortname']))


def dividends(secid):
    # Дивиденды по акциям
    # ** описания нет
    # secid = 'GAZP'
    method = "securities/%s/dividends" % secid
    j = query(method)
    flat = flatten(j, 'dividends')

    print(pd.DataFrame(flat))
    # print(pd.DataFrame(f, columns=['secid','shortname' ,'primary_boardid', 'type']))
    # print(json.dumps(j, ensure_ascii=False, indent=4, sort_keys=True))


if __name__ == '__main__':
    # dividends('GAZP')
    stock_list()
