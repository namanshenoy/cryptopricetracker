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
    'SET_ALERT': -1
}


def run_settings():
    """
    Put settings in envioronment variables
    """
    for k, v  in SETTINGS.items():
        os.environ[k] = v