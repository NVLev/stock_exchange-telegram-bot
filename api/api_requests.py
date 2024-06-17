
from config_data.config import API_BASE_URL
import pandas as pd
import json
import requests
from urllib import parse

pd.set_option("display.max_columns", 15)
# Список бумаг торгуемых на московской бирже
    # https://iss.moex.com/iss/reference/5
    # r_list = query("securities")
    #r_list = query("securities", q="сбер")  # q='' - поиск всех бумаг, содержащих ''
    # j = query("securities", group_by="type", group_by_filter="corporate_bond", limit=10)
    # j = query("securities", q="втб", group_by="type", group_by_filter="corporate_bond", limit=10)
    #flat = flatten(r_list, 'securities')

    # Спецификация инструмента
    # https://iss.moex.com/iss/reference/13
    # secid = 'SBER'
    # method = "securities/%s" % secid
    # j = query(method)
    # flat = flatten(j, 'description')

    # Купоны по облигациям
    # ** описания нет
    # secid = 'RU000A102QJ7'
    # method = "securities/%s/bondization" % secid
    # j = query(method)
    # f = flatten(j, 'coupons')


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
    return [{k: r[i] for i, k in enumerate(response_dict[blockname]['columns'])} for r in response_dict[blockname]['data']]


def dividends(secid):

    # Дивиденды по акциям
    # ** описания нет
    # secid = 'GAZP'
    method = "securities/%s/dividends" % secid
    j = query(method)
    flat = flatten(j, 'dividends')

    return (pd.DataFrame(flat))
    # print(pd.DataFrame(f, columns=['secid','shortname' ,'primary_boardid', 'type']))
    # print(json.dumps(j, ensure_ascii=False, indent=4, sort_keys=True))


# if __name__ == '__main__':
    # dividends('GAZP')
