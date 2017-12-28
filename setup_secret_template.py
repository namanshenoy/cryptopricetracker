"""
SETTINGS TEMPLATE.
Duplicate this file and fill out the settings
"""
import os

SETTINGS = {
    'ACCOUNT_SID' : 'ACXXXXXXXXX-TEMPLATE',
    'AUTH_TOKEN' : 'XXXXXXXXX-TEMPLATE',
    'SEND_TO_PHONE': '+1XXXXXXXX-TEMPLATE',
    'SEND_FROM_PHONE': '+1XXXXXXXX-TEMPLATE',
    'SET_ALERT': -1,
    'NEXT_ALERT': 10
}

PORTFOLIO = {
        "brdbtc":{
            "name":"BRD",
            "conv":"BTC",
            "quan":100,
            "code":"brdbtc",
            "notify":True
        },
        "xvgbtc":{
            "name":"XVG",
            "conv":"BTC",
            "quan":1000,
            "code":"xvgbtc",
            "notify":False
        }
}


def run_settings():
    """
    Put settings in envioronment variables
    """
    for k, v  in SETTINGS.items():
        os.environ[k] = v