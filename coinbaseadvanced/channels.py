from models.market_data import HeartbeatEvent, CandlesEvent, MarketTradesEvent, StatusEvent, TickerEvent, \
    TickerBatchEvent, Level2Event, UserEvent

# Mapping of channel names to their corresponding event classes.
# https://docs.cdp.coinbase.com/advanced-trade/docs/ws-channels/#heartbeats-channel
CHANNELS = {
    'heartbeat': HeartbeatEvent,  # Channel for heartbeat events
    'candles': CandlesEvent,  # Channel for candle events (OHLC data)
    'market_trades': MarketTradesEvent,  # Channel for market trades events
    'status': StatusEvent,  # Channel for status events (e.g., product status)
    'ticker': TickerEvent,  # Channel for ticker events (price and volume data)
    'ticker_batch': TickerBatchEvent,  # Channel for batch ticker events
    'l2_data': Level2Event,  # Channel for level 2 data events (order book updates)
    'user': UserEvent,  # Channel for user-specific events (e.g., orders, positions)
}
