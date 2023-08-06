from blankly import Screener, Oanda, ScreenerState
from blankly.indicators import rsi


def is_stock_buy(symbol, state: ScreenerState):
    # in here we can get the price data, do anything else that we may need
    prices = state.interface.history(symbol, 40, resolution='1d')
    rsi_values = rsi(prices['close'], 14)
    return {'is_oversold': rsi_values.iloc[-1] < 30, 'price': prices.iloc[-1]['close']}


def formatter(results, state: ScreenerState):
    # here we can format the results on a per ticker basis
    result_string = 'These are all the stocks that are current oversold: \n'
    for symbol, result in results.items():
        if result['is_oversold']:
            result_string += '{} is currently oversold at a price of {}\n\n'.format(symbol, result['price'])
    print(result_string)
    return result_string


if __name__ == "__main__":
    # Authenticate Oanda strategy
    exchange = Oanda()
    tickers = [x['symbol'] for x in exchange.interface.get_products()]
    screener = Screener(exchange, is_stock_buy, symbols=tickers, formatter=formatter)
    screener.notify()
