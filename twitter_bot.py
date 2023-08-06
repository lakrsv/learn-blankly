import blankly


class TwitterBot(blankly.Model):
    def main(self, args):
        while self.has_data:
            self.sleep('1h')
            self.backtester.value_account()

    def event(self, type_: str, data: any):
        if type_ == "tweet":
            if 'twitter' in data.lower():
                price = self.interface.get_price('TWTR')
                print("Buying twitter...")
                self.interface.market_order('TWTR', 'buy', blankly.trunc(
                    (self.interface.cash / price) * 0.2, 2))
            else:
                print("Message did not contain twitter")


if __name__ == "__main__":
    exchange = blankly.Alpaca()
    model = TwitterBot(exchange)

    model.backtester.add_custom_events((blankly.data.JsonEventReader('./tweets.json')))
    model.backtester.add_prices('TWTR', '1h', start_date='1/3/23', stop_date='1/4/23')

    print(model.backtest(args=None, initial_values={'USD': 10000}))
