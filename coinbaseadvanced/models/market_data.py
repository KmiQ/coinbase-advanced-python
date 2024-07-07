class Level2Event:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.events = [L2Event(event) for event in events]

    def __repr__(self):
        return f"Level2Event(channel={self.channel}, events={self.events})"

class L2Event:
    def __init__(self, event: dict):
        self.type = event.get('type')
        self.product_id = event.get('product_id')
        self.updates = [L2Update(update) for update in event.get('updates', [])]

    def __repr__(self):
        return f"L2Event(type={self.type}, product_id={self.product_id}, updates={self.updates})"

class L2Update:
    def __init__(self, update: dict):
        self.side = update.get('side')
        self.event_time = update.get('event_time')
        self.price_level = update.get('price_level')
        self.new_quantity = update.get('new_quantity')

    def __repr__(self):
        return f"L2Update(side={self.side}, event_time={self.event_time}, price_level={self.price_level}, new_quantity={self.new_quantity})"


class MarketUpdate:
    def __init__(self, update: dict):
        self.side = update.get('side')
        self.event_time = update.get('event_time')
        self.price_level = update.get('price_level')
        self.new_quantity = update.get('new_quantity')

    def __repr__(self):
        return f"MarketUpdate(side={self.side}, event_time={self.event_time}, price_level={self.price_level}, new_quantity={self.new_quantity})"

class HeartbeatEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int):
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num

    def __repr__(self):
        return f"HeartbeatEvent(channel={self.channel}, timestamp={self.timestamp}, sequence_num={self.sequence_num})"

class CandlesEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.candles = []
        for event in events:
            if 'candles' in event:
                self.candles.extend([CandleUpdate(update) for update in event['candles']])

    def __repr__(self):
        return f"CandlesEvent(channel={self.channel}, candles={self.candles})"

class CandleUpdate:
    def __init__(self, update: dict):
        self.start = update['start']
        self.high = update['high']
        self.low = update['low']
        self.open = update['open']
        self.close = update['close']
        self.volume = update['volume']
        self.product_id = update['product_id']

    def __repr__(self):
        return (f"CandleUpdate(start={self.start}, high={self.high}, low={self.low}, open={self.open}, "
                f"close={self.close}, volume={self.volume}, product_id={self.product_id})")

class MarketTradesEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, trades: list):
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.trades = [TradeDetail(trade) for trade in trades]

    def __repr__(self):
        return f"MarketTradesEvent(channel={self.channel}, trades={self.trades})"

class TradeDetail:
    def __init__(self, trade: dict):
        self.trade_id = trade.get('trade_id')
        self.product_id = trade.get('product_id')
        self.price = trade.get('price')
        self.size = trade.get('size')
        self.side = trade.get('side')
        self.time = trade.get('time')

    def __repr__(self):
        return f"TradeDetail(product_id={self.product_id} trade_id={self.trade_id}, price={self.price}, size={self.size}, side={self.side}, time={self.time})"

class StatusEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.products = []
        for event in events:
            if 'products' in event:
                self.products.extend([ProductStatus(product) for product in event['products']])

    def __repr__(self):
        return f"StatusEvent(channel={self.channel}, products={self.products})"

class ProductStatus:
    def __init__(self, product: dict):
        self.product_id = product.get('id')
        self.status = product.get('status')
        self.product_type = product.get('product_type')
        self.base_currency = product.get('base_currency')
        self.quote_currency = product.get('quote_currency')
        self.base_increment = product.get('base_increment')
        self.quote_increment = product.get('quote_increment')
        self.display_name = product.get('display_name')
        self.status_message = product.get('status_message')
        self.min_market_funds = product.get('min_market_funds')

    def __repr__(self):
        return f"ProductStatus(product_id={self.product_id}, status={self.status}, product_type={self.product_type}, base_currency={self.base_currency}, quote_currency={self.quote_currency}, base_increment={self.base_increment}, quote_increment={self.quote_increment}, display_name={self.display_name}, status_message={self.status_message}, min_market_funds={self.min_market_funds})"

class TickerEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.tickers = []
        for event in events:
            if 'tickers' in event:
                self.tickers.extend([TickerDetail(ticker) for ticker in event['tickers']])

    def __repr__(self):
        return f"TickerEvent(channel={self.channel}, tickers={self.tickers})"

class TickerDetail:
    def __init__(self, ticker: dict):
        self.type = ticker.get('type')
        self.product_id = ticker.get('product_id')
        self.price = ticker.get('price')
        self.volume_24_h = ticker.get('volume_24_h')
        self.low_24_h = ticker.get('low_24_h')
        self.high_24_h = ticker.get('high_24_h')
        self.low_52_w = ticker.get('low_52_w')
        self.high_52_w = ticker.get('high_52_w')
        self.price_percent_chg_24_h = ticker.get('price_percent_chg_24_h')
        self.best_bid = ticker.get('best_bid')
        self.best_ask = ticker.get('best_ask')
        self.best_bid_quantity = ticker.get('best_bid_quantity')
        self.best_ask_quantity = ticker.get('best_ask_quantity')

    def __repr__(self):
        return (f"TickerDetail(type={self.type}, product_id={self.product_id}, price={self.price}, "
                f"volume_24_h={self.volume_24_h}, low_24_h={self.low_24_h}, high_24_h={self.high_24_h}, "
                f"low_52_w={self.low_52_w}, high_52_w={self.high_52_w}, price_percent_chg_24_h={self.price_percent_chg_24_h}, "
                f"best_bid={self.best_bid}, best_ask={self.best_ask}, best_bid_quantity={self.best_bid_quantity}, "
                f"best_ask_quantity={self.best_ask_quantity})")

class TickerBatchEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.tickers = []
        for event in events:
            if 'tickers' in event:
                self.tickers.extend([TickerDetail(ticker) for ticker in event['tickers']])

    def __repr__(self):
        return f"TickerBatchEvent(channel={self.channel}, tickers={self.tickers})"