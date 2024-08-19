from models.market_data import HeartbeatEvent, CandlesEvent, MarketTradesEvent, StatusEvent, TickerEvent, \
    TickerBatchEvent, Level2Event, UserEvent

# Mapping of channel names to their corresponding event classes.
# https://docs.cdp.coinbase.com/advanced-trade/docs/ws-channels/#heartbeats-channel
CHANNELS = {
    'heartbeat': HeartbeatEvent,  # Channel for heartbeat events
    'candles': CandlesEvent,  # Real-time updates on product candles
    'market_trades': MarketTradesEvent,  # Real-time updates every time a market trade happens
    'status': StatusEvent,  # Sends all products and currencies on a preset interval
    'ticker': TickerEvent,  # Real-time price updates every time a match happens
    'ticker_batch': TickerBatchEvent,  # Real-time price updates every 5000 milliseconds
    'l2_data': Level2Event,  # All updates and easiest way to keep order book snapshot
    'user': UserEvent,  # Only sends messages that include the authenticated user
}
