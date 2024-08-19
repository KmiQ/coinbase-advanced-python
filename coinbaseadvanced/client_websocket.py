import json
import time
import threading
import websocket
from channels import CHANNELS
from models.market_data import HeartbeatEvent
from utils import generate_jwt


class CoinbaseWebSocketClient:
    def __init__(self, api_key: str, signing_key: str, ws_url: str = "wss://advanced-trade-ws.coinbase.com"):
        """
        Initializes the CoinbaseWebSocketClient with API key, signing key, and WebSocket URL.

        :param api_key: The API key for Coinbase.
        :param signing_key: The signing key for generating JWT.
        :param ws_url: The WebSocket URL for connecting to Coinbase. Defaults to the advanced trade WebSocket URL.
        """
        self.api_key = api_key
        self.signing_key = signing_key
        self.ws_url = ws_url
        self.callbacks = {}

    def _create_message(self, message_type: str, product_ids: list, channel: str) -> dict:
        """
        Creates a subscription message to send to the WebSocket.

        :param message_type: The type of message (e.g., "subscribe").
        :param product_ids: List of product IDs to subscribe to.
        :param channel: The channel to subscribe to.
        :return: A dictionary containing the subscription message.
        """
        jwt_token = generate_jwt(self.api_key, self.signing_key)
        return {
            "type": message_type,
            "product_ids": product_ids,
            "channel": channel,
            "jwt": jwt_token,
            "timestamp": int(time.time())
        }

    def _handle_message(self, ws, message: str):
        """
        Handles incoming WebSocket messages.

        :param ws: The WebSocket instance.
        :param message: The message received from the WebSocket.
        :return: The event object created from the message or None if the message type is not recognized.
        """
        data = json.loads(message)

        if 'type' in data and data['type'] == 'error':
            raise ValueError(f"Error message: {data['message']}")

        if 'channel' in data and data['channel'] == 'subscriptions':
            return data

        if 'channel' in data and data['channel'] == 'heartbeats':
            heartbeat_event = HeartbeatEvent(
                channel=data['channel'],
                current_time=data['events'][0]['current_time'],
                heartbeat_counter=data['events'][0]['heartbeat_counter']
            )
            if 'heartbeats' in self.callbacks:
                self.callbacks['heartbeats'](heartbeat_event)
            return heartbeat_event

        channel = data.get('channel')
        if channel and channel in CHANNELS:
            event_class = CHANNELS[channel]
            try:
                event = event_class(**data)
                if channel in self.callbacks:
                    self.callbacks[channel](event)
                return event
            except TypeError as e:
                raise TypeError(f"Error creating event for channel {channel}: {e}")
        else:
            raise ValueError(f"Unrecognized channel: {channel}")

    def subscribe(self, product_ids: list, channel: str, callback=None):
        """
        Subscribes to a specified channel for a list of product IDs and sets a callback for handling messages.

        :param product_ids: List of product IDs to subscribe to.
        :param channel: The channel to subscribe to.
        :param callback: Optional callback function to handle messages from the channel.
        """
        if callback:
            self.callbacks[channel] = callback

        def run():
            ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=self._handle_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            ws.on_open = lambda ws: self._on_open(ws, product_ids, channel)
            ws.run_forever()

        thread = threading.Thread(target=run)
        thread.start()

    def _on_open(self, ws, product_ids: list, channel: str):
        """
        Handles the WebSocket connection opening by sending subscription messages.

        :param ws: The WebSocket instance.
        :param product_ids: List of product IDs to subscribe to.
        :param channel: The channel to subscribe to.
        """
        subscribe_message = self._create_message("subscribe", product_ids, channel)
        ws.send(json.dumps(subscribe_message))
        heartbeat_message = self._create_message("subscribe", product_ids, "heartbeats")
        ws.send(json.dumps(heartbeat_message))

    def _on_error(self, ws, error: str):
        """
        Handles errors from the WebSocket.

        :param ws: The WebSocket instance.
        :param error: The error message.
        """
        raise Exception(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        """
        Handles the WebSocket connection closing.

        :param ws: The WebSocket instance.
        :param close_status_code: The status code for the connection closure.
        :param close_msg: The message for the connection closure.
        """
        raise Exception(f"Closed connection with status: {close_status_code}, message: {close_msg}")