from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
from ws4py import format_addresses, configure_logger
import json
import requests

logger = configure_logger()

manager = WebSocketManager()

BTC_USD = 0.0

def get_btc_usd():
    response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/sell")
    try:
        global BTC_USD
        BTC_USD = float(response.json()['data']['amount'])
        logger.info("Updated BTC Value: {}".format(BTC_USD))
    except Exception as e:
        logger.warning("BTC Value could not updated \n{}".format(str(e)))
        pass


class CryptoClient(WebSocketBaseClient): 
    def set_info(self, from_crypto, to_crypto):
        self.from_crypto = from_crypto
        self.to_crypto = to_crypto

    def handshake_ok(self):
        logger.info("Opening %s" % format_addresses(self))
        manager.add(self)

    def received_message(self, msg):
        event = json.loads(str(msg))
        print("{0}-{1} USD: {2:.2f}".format(self.from_crypto.upper(), self.to_crypto.upper(), float(event['k']['c'])* BTC_USD))


if __name__ == '__main__':
    import time
    import threading
    get_btc_usd()
    threading.Timer(10.0, get_btc_usd).start()

    try:
        manager.start() 
        client = CryptoClient('wss://stream.binance.com:9443/ws/ethbtc@kline_1m')
        client.set_info(from_crypto='ETH', to_crypto='BTC')
        client.connect()

        client = CryptoClient('wss://stream.binance.com:9443/ws/brdbtc@kline_1m')
        client.set_info(from_crypto='BRD', to_crypto='BTC')
        client.connect()

        while True:
            for ws in manager.websockets.values():
                if not ws.terminated:
                    break
            else:
                break
            print("NEXT SET")
            time.sleep(3)
    except KeyboardInterrupt:
        manager.close_all()
        manager.stop()
        manager.join()

