from models.market_data import HeartbeatEvent, CandlesEvent, MarketTradesEvent, StatusEvent, TickerEvent, \
    TickerBatchEvent, Level2Event

CHANNELS = {
    'heartbeat': HeartbeatEvent,
    'candles': CandlesEvent,
    'market_trades': MarketTradesEvent,
    'status': StatusEvent,
    'ticker': TickerEvent,
    'ticker_batch': TickerBatchEvent,
    "l2_data": Level2Event,
}
