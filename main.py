import requests
from application_info import BINANCE_API_URL


def get_futures_ticker_list():
    response = requests.get(BINANCE_API_URL)
    md = response.json()
    symbols = md['symbols']
    futures_list = []
    for symbol in symbols:
        if symbol['isMarginTradingAllowed'] and 'USDT' in symbol['symbol']:
            futures_list.append(symbol['baseAsset'])
    return futures_list


if __name__ == '__main__':
    print(get_futures_ticker_list())
    print(len(get_futures_ticker_list()))
