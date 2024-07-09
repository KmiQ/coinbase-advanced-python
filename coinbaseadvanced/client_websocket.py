import json
import time
import threading
import websocket
from channels import CHANNELS
from utils import generate_jwt


class CoinbaseWebSocketClient:
    def __init__(self, api_key: str, signing_key: str, ws_url: str = "wss://advanced-trade-ws.coinbase.com"):
        self.api_key = api_key
        self.signing_key = signing_key
        self.ws_url = ws_url
        self.callbacks = {}

    def _create_message(self, message_type: str, product_ids: list, channel: str) -> dict:
        jwt_token = generate_jwt(self.api_key, self.signing_key)
        message = {
            "type": message_type,
            "product_ids": product_ids,
            "channel": channel,
            "jwt": jwt_token,
            "timestamp": int(time.time())
        }
        return message

    def _handle_message(self, ws, message):
        print(f"Received raw message: {message}")  # Debug: print raw message
        data = json.loads(message)

        if 'type' in data and data['type'] == 'error':
            print(f"Error message: {data['message']}")
            return data

        # Gestione dei messaggi di sottoscrizione
        if 'channel' in data and data['channel'] == 'subscriptions':
            print(f"Subscriptions message: {data}")
            return data

        # Gestione del battito cardiaco
        if 'type' in data and data['type'] == 'heartbeat':
            self._handle_heartbeat(ws, message)
            return data

        channel = data.get('channel')
        if channel:
            if channel in CHANNELS:
                event_class = CHANNELS[channel]
                try:
                    event = event_class(**data)
                    print(event)
                    return event
                except TypeError as e:
                    print(f"Error creating event for channel {channel}: {e}")
                    return None
            else:
                print(f"Unrecognized channel: {channel}")
        else:
            print(f"Channel not specified in message: {data}")
        return None

    def subscribe(self, product_ids: list, channel: str, callback=None):
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

    def _on_open(self, ws, product_ids, channel):
        subscribe_message = self._create_message("subscribe", product_ids, channel)
        ws.send(json.dumps(subscribe_message))
        print(f"Sent subscribe message: {subscribe_message}")

    def _on_error(self, ws, error):
        print(f"Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print(f"Closed connection with status: {close_status_code}, message: {close_msg}")

    @staticmethod
    def _handle_heartbeat(self, ws, message):
        pass
