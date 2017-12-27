from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
from ws4py import format_addresses, configure_logger
import json
import requests

logger = configure_logger()

manager = WebSocketManager()

#FIXME: Change this global to local variable
BTC_USD = 0.0

def get_btc_usd():
    """
    Updates global BTC-USD conversion variable. Global only for dev purposes
    """
    response = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/sell")
    try:
        global BTC_USD
        BTC_USD = float(response.json()['data']['amount'])
        logger.info("Updated BTC Value: {}".format(BTC_USD))
    except Exception as e:
        logger.warning("BTC Value could not updated \n{}".format(str(e)))
        pass


class CryptoClient(WebSocketBaseClient):
    """
    Custom client for websockets.
        :param WebSocketBaseClient: 
    """

    def set_info(self, from_crypto, to_crypto, code=None):
        """
        Set From Conversion and To conversion cryptos, set universal conversion code
            :param self: 
            :param from_crypto: 
            :param to_crypto:
            :param code: 
        """   
        self.from_crypto = from_crypto
        self.to_crypto = to_crypto
        if code is not None:
            self.code = code
        else:
            self.code = from_crypto.lower()+to_crypto.lower()

    def handshake_ok(self):
        logger.info("Opening %s" % format_addresses(self))
        manager.add(self)

    def received_message(self, msg):
        """
        Method that gets fired when a message is recieved through websockets
            :param self: 
            :param msg: 
        """
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
        client.set_info(from_crypto='BRD', to_crypto='BTC', code='brdbtc')
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

