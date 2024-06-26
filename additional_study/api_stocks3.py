# import json
import datetime
from datetime import timedelta
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# request_url = ('https://iss.moex.com/iss/engines/stock/'
#                 'markets/shares/boards/TQBR/securities.json')
# arguments = {'securities.columns': ('SECID,'
#                                    'REGNUMBER,'
#                                      'LOTSIZE,'
#                                      'SHORTNAME')}
# with requests.Session() as session:
#     iss = apimoex.ISSClient(session, request_url, arguments)
#     data = iss.get()
#     df = pd.DataFrame(data['securities'])
#     df.set_index('SECID', inplace=True)
#     print(df.head(), '\n')
#     print(df.tail(), '\n')
#     df.info()

def stock_rate(asset):
    url = "https://iss.moex.com/iss/engines/stock/markets/" \
          "shares/boards/TQBR/securities.csv?iss.meta=off&iss." \
          "only=marketdata&marketdata.columns=SECID,LAST"
    quotes_csv_text = requests.get(url).text.split('\n')
    print(quotes_csv_text)
    for quotes_csv_line in quotes_csv_text:
        quotes_csv_tabl = quotes_csv_line.split(';')
        if quotes_csv_tabl[0] == asset:
            return float(quotes_csv_tabl[1])

if __name__ == '__main__':
    print(stock_rate('GAZP'))