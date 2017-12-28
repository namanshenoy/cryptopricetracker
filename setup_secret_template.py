"""
SETTINGS TEMPLATE.
Duplicate this file and fill out the settings
"""
import os

SETTINGS = {
    'ACCOUNT_SID' : 'ACXXXXXXXXX-TEMPLATE',
    'AUTH_TOKEN' : 'XXXXXXXXX-TEMPLATE',
    'SEND_TO_PHONE': '+1XXXXXXXX-TEMPLATE'
}


def run_settings():
    """
    Put settings in envioronment variables
    """
    for k in SETTINGS.keys():
        os.environ[k] = SETTINGS[k]
