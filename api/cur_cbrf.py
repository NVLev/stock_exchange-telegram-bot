import pandas as pd


def get_currency_rate(name_cur: str):
    try:
        url = 'http://www.cbr.ru/scripts/XML_daily.asp'
        raw = pd.read_xml(url, encoding='cp1251')
        df_new = raw[raw['Name'] == name_cur]
        if name_cur == 'Армянских драмов' or name_cur == 'Турецких лир':
            return (pd.DataFrame(df_new, columns=['CharCode', 'Nominal', 'Name', 'Value']))
        else:
            return (pd.DataFrame(df_new, columns=['CharCode', 'Name', 'Value']))
    except Exception as e:
        return "query error %s" % str(e)

