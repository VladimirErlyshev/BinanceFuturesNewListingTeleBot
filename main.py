import requests
import csv
from application_info import *


def get_futures_ticker_list() -> list:
    response = requests.get(BINANCE_API_URL)
    md = response.json()
    symbols = md['symbols']
    futures_list = []
    for symbol in symbols:
        if symbol['isMarginTradingAllowed'] and ('USDT' in symbol['symbol'] or 'USDC' in symbol['symbol']):
            futures_list.append(symbol['baseAsset'])

    return futures_list


def save_futures_list_to_file() -> None:
    with open('files/tickers.csv', 'w') as file:
        csv_writer = csv.writer(file)
        tickers_csv = [['ticker']]
        for ticker in get_futures_ticker_list():
            tickers_csv.append([ticker])
        csv_writer.writerows(tickers_csv)


def open_file_with_futures_tickers() -> list:
    tickers_list = []
    with open('files/tickers.csv', 'r') as file:
        csv_dict_reader = csv.DictReader(file)
        for row in csv_dict_reader:
            tickers_list.append(row["ticker"])

    return tickers_list


def detected_new_futures() -> str:
    set_for_api = set(get_futures_ticker_list())
    set_for_file = set(open_file_with_futures_tickers())
    if set_for_api == set_for_file:

        return 'Изменений в апи бинанса не обнаружено'

    elif len(set_for_api) > len(set_for_file):
        new_set = set_for_api.difference(set_for_file)
        save_futures_list_to_file()

        return f'Новые фьючерсы в апи бинанса {new_set}'

    else:
        new_set = set_for_file.difference(set_for_api)
        save_futures_list_to_file()

        return f'Отсутствуют фьючерсы в апи бинанса {new_set}'


if __name__ == '__main__':
    print(detected_new_futures())
