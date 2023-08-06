import blankly
from blankly import Strategy, StrategyState, Interface
from blankly import Alpaca
from blankly.utils import trunc
from blankly.indicators import sma


def init(symbol, state: StrategyState):
    interface: Interface = state.interface
    resolution: float = state.resolution
    variables = state.variables
    # initialize the historical data
    variables['history'] = interface.history(symbol, 800,
        resolution, return_as='list')['close']
    variables['has_bought'] = False


def price_event(price, symbol, state: StrategyState):
    interface: Interface = state.interface
    variables = state.variables

    variables['history'].append(price)

    sma200 = sma(variables['history'], period=200)
    # match up dimensions
    sma50 = sma(variables['history'], period=50)[-len(sma200):]
    diff = sma50 - sma200
    slope_sma50 = (sma50[-1] - sma50[-5]) / 5 # get the slope of the last 5 SMA50 Data Points
    prev_diff = diff[-2]
    curr_diff = diff[-1]
    is_cross_up = slope_sma50 > 0 > prev_diff and curr_diff >= 0
    is_cross_down = slope_sma50 < 0 < prev_diff and curr_diff <= 0
    # comparing prev diff with current diff will show a cross
    if is_cross_up and not variables['has_bought']:
        interface.market_order(symbol, 'buy', int(interface.cash/price))
        variables['has_bought'] = True
    elif is_cross_down and variables['has_bought']:
        # use strategy.base_asset if on CoinbasePro or Binance
        # truncate here to fix any floating point errors
        interface.market_order(symbol, 'sell', int(interface.account[str.split(symbol, '-')[0]].available))
        variables['has_bought'] = False


if __name__ == "__main__":
    # Authenticate Oanda strategy
    exchange = blankly.Oanda()

    # Use our strategy helper on Oanda
    strategy = blankly.Strategy(exchange)

    # Run the price event function every time we check for a new price - by default that is 15 seconds
    strategy.add_price_event(price_event, symbol='EUR-USD', resolution='15m', init=init)

    # Start our strategy, or run a backtest if this script is run locally.
    if blankly.is_deployed:
        strategy.start()
    else:
        print(strategy.backtest(to='1y', initial_values={'USD': 10000}))