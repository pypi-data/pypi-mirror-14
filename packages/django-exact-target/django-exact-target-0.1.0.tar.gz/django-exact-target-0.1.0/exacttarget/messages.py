from raven.contrib.django.raven_compat.models import client as raven_client
import requests
from . import token, exceptions


class TriggeredSend(object):
    url_base = 'https://www.exacttargetapis.com/messaging/v1/messageDefinitionSends'

    def __init__(self, external_key):
        self.external_key = external_key
        self.token = token.CachedTokenGenerator()


    def dispatch(self, email, attrs):
        url = '%s/key:%s/send' % (self.url_base, self.external_key)
        headers = self.token.headers()
        req_data = {
            "To": {
                "Address": email,
                "SubscriberKey": email,
                "ContactAttributes": {
                    "SubscriberAttributes": attrs
                },
            },
            "OPTIONS": {
                "RequestType": "SYNC"
            },
        }

        resp = requests.post(url, headers=headers, json=req_data)
        resp.raise_for_status()
        reply = resp.json()
        for response in reply['responses']:
            if response['hasErrors']:
                raven_client.captureMessage('Error occurred while submitting subscriber to exact target', extra=reply)
                messages = response.get('messageErrors', [])
                raise exceptions.TriggeredSendException(messages[0]['messageErrorStatus'] if len(messages) else 'Unknown TriggeredSend Error Occurred')
