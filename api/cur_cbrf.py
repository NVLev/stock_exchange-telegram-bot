import xml.etree.ElementTree as ET
from io import StringIO
import requests
import pandas as pd

def get_currency_rate(name_cur:str):
        try:
            url = 'http://www.cbr.ru/scripts/XML_daily.asp'
            raw = pd.read_xml(url, encoding='cp1251')

            # print(pd.read_xml(url, encoding='cp1251'))
            # print(pd.DataFrame(raw, columns=['CharCode', 'Name', 'Value']))
            df_new = raw[raw['Name'] == name_cur]
            if name_cur == 'Армянских драмов' or name_cur == 'Турецких лир':
                return (pd.DataFrame(df_new, columns=['CharCode', 'Nominal', 'Name', 'Value']))
            else:
                return (pd.DataFrame(df_new, columns=['CharCode', 'Name', 'Value']))
        except Exception as e:
                print("query error %s" % str(e))
                return None

print(get_currency_rate('Китайский Юань'))
