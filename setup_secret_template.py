"""
SETTINGS TEMPLATE.
Duplicate this file and fill out the settings
"""
import os

SETTINGS = {
    'ACCOUNT_SID' : 'ACXXXXXXXXX-TEMPLATE', # Twilio SID
    'AUTH_TOKEN' : 'XXXXXXXXX-TEMPLATE', # Twilio Auth Token
    'SEND_TO_PHONE': '+1XXXXXXXX-TEMPLATE', # Your phone number
    'SEND_FROM_PHONE': '+1XXXXXXXX-TEMPLATE', # Twilio Phone number
    'SET_ALERT_HIGH': "420", # Set high alert value as STRING
    'SET_ALERT_LOW': "-1", # Set low alert as STRING, -1 is no alerts for this catagory 
    'NEXT_ALERT': "10" # Increment value once SET_ALERT price has been reached STRING
}

PORTFOLIO = {
        "brdbtc":{ # name + market all small
            "name":"BRD", # Price ticker
            "conv":"BTC", # Market (Only BTC is supported right now)
            "quan":100, # Number of coins FLOAT
            "code":"brdbtc", # name + market all small
            "notify":True # True = Use in Binance total calculations and Text notification alerts
        },
        "xvgbtc":{
            "name":"XVG",
            "conv":"BTC",
            "quan":1000,
            "code":"xvgbtc",
            "notify":False # False = Remove from total Binance Value calculations and Text notifications alerts
        }
}


def run_settings():
    """
    Put settings in envioronment variables
    """
    for k, v  in SETTINGS.items():
        os.environ[k] = v