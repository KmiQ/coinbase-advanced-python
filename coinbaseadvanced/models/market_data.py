class Level2Event:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        """
        Initializes a Level2Event object.

        :param channel: The channel name.
        :param client_id: The client ID.
        :param timestamp: The timestamp of the event.
        :param sequence_num: The sequence number of the event.
        :param events: A list of event data.
        """
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.events = [L2Event(event) for event in events]

    def __repr__(self):
        return f"Level2Event(channel={self.channel}, events={self.events})"


class L2Event:
    def __init__(self, event: dict):
        """
        Initializes an L2Event object.

        :param event: A dictionary containing event data.
        """
        self.type = event.get('type')
        self.product_id = event.get('product_id')
        self.updates = [L2Update(update) for update in event.get('updates', [])]

    def __repr__(self):
        return f"L2Event(type={self.type}, product_id={self.product_id}, updates={self.updates})"


class L2Update:
    def __init__(self, update: dict):
        """
        Initializes an L2Update object.

        :param update: A dictionary containing update data.
        """
        self.side = update.get('side')
        self.event_time = update.get('event_time')
        self.price_level = update.get('price_level')
        self.new_quantity = update.get('new_quantity')

    def __repr__(self):
        return (f"L2Update(side={self.side}, event_time={self.event_time}, price_level={self.price_level}, "
                f"new_quantity={self.new_quantity})")


class HeartbeatEvent:
    def __init__(self, channel: str, current_time: str, heartbeat_counter: int):
        """
        Initializes a HeartbeatEvent object.

        :param channel: The channel name.
        :param current_time: The current time of the heartbeat event.
        :param heartbeat_counter: The heartbeat counter.
        """
        self.channel = channel
        self.current_time = current_time
        self.heartbeat_counter = heartbeat_counter

    def __repr__(self):
        return (f"HeartbeatEvent(channel={self.channel}, current_time={self.current_time}, "
                f"heartbeat_counter={self.heartbeat_counter})")


class CandlesEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        """
        Initializes a CandlesEvent object.

        :param channel: The channel name.
        :param client_id: The client ID.
        :param timestamp: The timestamp of the event.
        :param sequence_num: The sequence number of the event.
        :param events: A list of event data.
        """
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
        """
        Initializes a CandleUpdate object.

        :param update: A dictionary containing update data.
        """
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
        """
        Initializes a MarketTradesEvent object.

        :param channel: The channel name.
        :param client_id: The client ID.
        :param timestamp: The timestamp of the event.
        :param sequence_num: The sequence number of the event.
        :param trades: A list of trade data.
        """
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.trades = [TradeDetail(trade) for trade in trades]

    def __repr__(self):
        return f"MarketTradesEvent(channel={self.channel}, trades={self.trades})"


class TradeDetail:
    def __init__(self, trade: dict):
        """
        Initializes a TradeDetail object.

        :param trade: A dictionary containing trade data.
        """
        self.trade_id = trade.get('trade_id')
        self.product_id = trade.get('product_id')
        self.price = trade.get('price')
        self.size = trade.get('size')
        self.side = trade.get('side')
        self.time = trade.get('time')

    def __repr__(self):
        return f"TradeDetail(product_id={self.product_id}, trade_id={self.trade_id}, price={self.price}, size={self.size}, side={self.side}, time={self.time})"


class StatusEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        """
        Initializes a StatusEvent object.

        :param channel: The channel name.
        :param client_id: The client ID.
        :param timestamp: The timestamp of the event.
        :param sequence_num: The sequence number of the event.
        :param events: A list of event data.
        """
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
        """
        Initializes a ProductStatus object.

        :param product: A dictionary containing product data.
        """
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
        return (f"ProductStatus(product_id={self.product_id}, status={self.status}, product_type={self.product_type}, "
                f"base_currency={self.base_currency}, quote_currency={self.quote_currency}, base_increment={self.base_increment}, "
                f"quote_increment={self.quote_increment}, display_name={self.display_name}, status_message={self.status_message}, "
                f"min_market_funds={self.min_market_funds})")


class TickerEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list):
        """
        Initializes a TickerEvent object.

        :param channel: The channel name.
        :param client_id: The client ID.
        :param timestamp: The timestamp of the event.
        :param sequence_num: The sequence number of the event.
        :param events: A list of event data.
        """
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
        """
        Initializes a TickerDetail object.

        :param ticker: A dictionary containing ticker data.
        """
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
        """
        Initializes a TickerBatchEvent object.

        :param channel: The channel name.
        :param client_id: The client ID.
        :param timestamp: The timestamp of the event.
        :param sequence_num: The sequence number of the event.
        :param events: A list of event data.
        """
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


class UserEvent:
    def __init__(self, channel: str, client_id: str, timestamp: str, sequence_num: int, events: list, user_id: str = None, profile_id: str = None):
        """
        Initializes a UserEvent object.

        :param channel: The channel name.
        :param client_id: The client ID.
        :param timestamp: The timestamp of the event.
        :param sequence_num: The sequence number of the event.
        :param events: A list of event data.
        :param user_id: The user ID.
        :param profile_id: The profile ID.
        """
        self.channel = channel
        self.client_id = client_id
        self.timestamp = timestamp
        self.sequence_num = sequence_num
        self.user_id = user_id
        self.profile_id = profile_id
        self.orders = []
        self.positions = {"perpetual_futures_positions": [], "expiring_futures_positions": []}
        for event in events:
            if 'orders' in event:
                self.orders.extend([Order(order) for order in event['orders']])
            if 'positions' in event:
                self.positions = event['positions']

    def __repr__(self):
        return f"UserEvent(channel={self.channel}, user_id={self.user_id}, profile_id={self.profile_id}, orders={self.orders}, positions={self.positions})"


class Order:
    def __init__(self, order: dict):
        """
        Initializes an Order object.

        :param order: A dictionary containing order data.
        """
        self.avg_price = order.get('avg_price')
        self.cancel_reason = order.get('cancel_reason')
        self.client_order_id = order.get('client_order_id')
        self.completion_percentage = order.get('completion_percentage')
        self.contract_expiry_type = order.get('contract_expiry_type')
        self.cumulative_quantity = order.get('cumulative_quantity')
        self.filled_value = order.get('filled_value')
        self.leaves_quantity = order.get('leaves_quantity')
        self.limit_price = order.get('limit_price')
        self.number_of_fills = order.get('number_of_fills')
        self.order_id = order.get('order_id')
        self.order_side = order.get('order_side')
        self.order_type = order.get('order_type')
        self.outstanding_hold_amount = order.get('outstanding_hold_amount')
        self.post_only = order.get('post_only')
        self.product_id = order.get('product_id')
        self.product_type = order.get('product_type')
        self.reject_reason = order.get('reject_reason')
        self.retail_portfolio_id = order.get('retail_portfolio_id')
        self.risk_managed_by = order.get('risk_managed_by')
        self.status = order.get('status')
        self.stop_price = order.get('stop_price')
        self.time_in_force = order.get('time_in_force')
        self.total_fees = order.get('total_fees')
        self.total_value_after_fees = order.get('total_value_after_fees')
        self.trigger_status = order.get('trigger_status')
        self.creation_time = order.get('creation_time')
        self.end_time = order.get('end_time')
        self.start_time = order.get('start_time')

    def __repr__(self):
        return (f"Order(order_id={self.order_id}, order_side={self.order_side}, order_type={self.order_type}, "
                f"status={self.status}, product_id={self.product_id}, limit_price={self.limit_price}, "
                f"leaves_quantity={self.leaves_quantity}, creation_time={self.creation_time})")
