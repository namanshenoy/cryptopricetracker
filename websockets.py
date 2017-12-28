# pylint: disable-msg=C0103

import json
from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
from ws4py import format_addresses, configure_logger
import requests

LOGGER = configure_logger()

MANAGER = WebSocketManager()

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
        LOGGER.info("Updated BTC Value: %f" % float(BTC_USD))
    except Exception as e:
        LOGGER.warning("BTC Value could not updated \n{}".format(str(e)))
        pass


class CryptoClient(WebSocketBaseClient):
    """
    Custom client for websockets.
        :param WebSocketBaseClient: Superclas for WebSocketClient from ws4py
    """

    def set_info(self, from_crypto, to_crypto, code=None):
        """
        Set From Conversion and To conversion cryptos, set universal conversion code
            :param self:.
            :param from_crypto: Cryto ticker from which to convert
            :param to_crypto: Cryto ticker to which to convert
            :param code: Unique identifier for this conversion
        """ 
        self.from_crypto = from_crypto
        self.to_crypto = to_crypto
        if code is not None:
            self.code = code
        else:
            self.code = from_crypto.lower()+to_crypto.lower()

    def handshake_ok(self):
        LOGGER.info("Opening %s" % format_addresses(self))
        MANAGER.add(self)

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

    my_coins = [
        {
            "name":"BRD",
            "conv":"BTC",
            "quan":51.948,
            "code":"brdbtc"
        },
        {
            "name":"XVG",
            "conv":"BTC",
            "quan":466.794,
            "code":"xvgbtc"
        },
        {
            "name":"ADA",
            "conv":"BTC",
            "quan":50.949,
            "code":"adabtc"
        },
        {
            "name":"NEO",
            "conv":"BTC",
            "quan":0.789865,
            "code":"neobtc"
        },
         {
            "name":"XRP",
            "conv":"BTC",
            "quan":73.926,
            "code":"xrpbtc"
        },
        {
            "name":"IOTA",
            "conv":"BTC",
            "quan":6.993,
            "code":"iotabtc"
        }
    ]

    try:
        MANAGER.start()
        CLIENT = CryptoClient('wss://stream.binance.com:9443/ws/ethbtc@kline_1m')
        CLIENT.set_info(from_crypto='ETH', to_crypto='BTC')
        CLIENT.connect()

        CLIENT = CryptoClient('wss://stream.binance.com:9443/ws/brdbtc@kline_1m')
        CLIENT.set_info(from_crypto='BRD', to_crypto='BTC', code='brdbtc')
        CLIENT.connect()

        while True:
            for ws in MANAGER.websockets.values():
                if not ws.terminated:
                    break
            else:
                break
            print("NEXT SET")
            time.sleep(3)
    except KeyboardInterrupt:
        MANAGER.close_all()
        MANAGER.stop()
        MANAGER.join()