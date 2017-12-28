""" Client Wrapper for Twilio API to send messages """
import os
from twilio.rest import Client

class TwilioClient():
    """
    Client wrapper for Twilio Message API
    """
    def __init__(self):
        self.account_sid = os.environ['ACCOUNT_SID']
        self.auth_token = os.environ['AUTH_TOKEN']
        self.my_phone = os.environ['SEND_TO_PHONE']
        self.client = Client(self.account_sid, self.auth_token)


    def send_sms(self, message):
        """
        Sends message using Twilio API
            :param self:
            :param message: Message to send
        """
        self.client.messages.create(
            to=self.my_phone,
            from_="+17745412752",
            body=message
        )