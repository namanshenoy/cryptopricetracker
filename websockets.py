""" Sets up websockets for Dashboard """
# pylint: disable-msg=C0103

import json
import os
from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
from ws4py import format_addresses, configure_logger
import queue
import requests

LOGGER = configure_logger()

MANAGER = WebSocketManager()

coin_queue = queue.Queue()

#FIXME: Change these global to local variable
BTC_USD = 0.0

class SetQueue():
    """
    Custom Queue that uses a set instead of a regular queue. This keeps a set of coin names as well as a dict of it's coin:value
        :param queue.Queue: 
    """
    def __init__(self):
        self.queue = set()
        self.values = dict({})

    def put(self, item, value):
        self.queue.add(item)
        self.values[item] = value

    def get(self):
        item = self.queue.pop()
        value = self.values[item]
        del self.values[item]
        return item.value

    def _size(self):
        return len(self.queue)

coin_queue = SetQueue()

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

    def set_info(self, from_crypto, to_crypto, code=None, amount=0):
        """
        Set From Conversion and To Conversion cryptos, set universal conversion code
            :param self:.
            :param from_crypto: Cryto ticker from which to convert
            :param to_crypto: Cryto ticker to which to convert
            :param code: Unique identifier for this conversion
            :param amount: Amount of coins held
        """ 
        self.from_crypto = from_crypto
        self.to_crypto = to_crypto
        self.amount = amount
        self.btc_value = 0
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
        self.btc_value = float(event['k']['c'])
        coin_queue.put(self.code, self.btc_value)
        #print("{0}-{1} USD: {2:.2f}".format(self.from_crypto.upper(), self.to_crypto.upper(), float(event['k']['c'])* BTC_USD * self.amount))

    def get_btc_value(self):
        """
        docstring here
            :param self: 
            :return: Returns tuple of Unique Conversion identifier and value of coin in BTC
            :type: tuple(str, float)
        """   
        if self.code is None or self.btc_value is None:
            return None, None
        return self.code, self.btc_value

if __name__ == '__main__':
    import time
    import threading
    import setup_secret
    import send_sms

    setup_secret.run_settings()
    sms_client = send_sms.TwilioClient()
    ALERT_PRICE = float(os.environ['SET_ALERT'])
    ALERT_UPDATE_VAL = float(os.environ['NEXT_ALERT'])

    #sms_client.send_sms("This shit worked!")
    
    get_btc_usd()
    threading.Timer(10.0, get_btc_usd).start()

    my_coins = setup_secret.PORTFOLIO


    try:
        MANAGER.start()
        for coin in my_coins.values():
            client = CryptoClient('wss://stream.binance.com:9443/ws/{0}@kline_1m'.format(coin['code']))
            client.set_info(from_crypto=coin['name'], to_crypto=coin['conv'], amount=coin['quan'])
            coin, btc_val = client.get_btc_value()
            coin_queue.values[coin] = btc_val
            client.connect()

        while True:
            for ws in MANAGER.websockets.values():
                coin, btc_val = ws.get_btc_value()
                coin_queue.values[coin] = btc_val
                if not ws.terminated:
                    break
                else:
                    break

            os.system("clear")

            total_val = 0.
            total_btc = 0.
            for coin in coin_queue.values:
                current_val = float(coin_queue.values[coin])* BTC_USD * my_coins[coin]['quan']
                if my_coins[coin]['notify']:
                    total_val+= current_val
                    total_btc+= float(coin_queue.values[coin]) * my_coins[coin]['quan']
                print("{0} - {1} USD: {2:.2f}\t|\tSingle: {3:.4f}".format(coin.upper()[:-3], "BTC", current_val, coin_queue.values[coin]*BTC_USD))
            print ("Total Binance Value : {0:.2f}".format(total_val))
            print("Total Value in Bitcoin: {0:.8f}\n(USD/BTC from Coinbase)".format(total_btc))
            if ALERT_PRICE is not -1 and total_val >= ALERT_PRICE:
                sms_client.send_sms("Your portfolio has reached {0}.\nNext text notification set to: {1}".format(ALERT_PRICE, ALERT_UPDATE_VAL+ALERT_PRICE))
                ALERT_PRICE += ALERT_UPDATE_VAL
            time.sleep(3)

    except KeyboardInterrupt:
        MANAGER.close_all()
        MANAGER.stop()
        MANAGER.join()