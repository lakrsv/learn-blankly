import blankly
from blankly import CoinbasePro, Strategy, StrategyState


def init(symbol, state: StrategyState):
    # get last 150 data points
    state.variables['history'] = state.interface.history(symbol, 150, state.resolution)
    state.variables['has_position'] = False
    state.variables['TP'] = 0


def custom_price_event(price, symbol, state: StrategyState):
    # do something here
    pass


def teardown(symbol, state: StrategyState):
    if state.variables['has_position']:
        state.interface.market_order(symbol, 'sell', state.interface.account[symbol].available)


if __name__ == '__main__':
    # Authenticate oanda exchange
    exchange = blankly.Oanda()

    # Use our strategy helper on coinbase pro
    strategy = blankly.Strategy(exchange)
    strategy.add_price_event(custom_price_event, 'EUR-USD', resolution='1h', init=init, teardown=teardown)
    strategy.add_price_event(custom_price_event, 'AUD-USD', resolution='1h', init=init, teardown=teardown)

    strategy.start()
