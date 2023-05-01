from django.conf import settings
import json
import base64
import hmac
import hashlib
from emailhooks.tasks import handler_tasks


class PayloadDispatcher:
    '''Provides dispatching of payload to different handlers'''

    # custom event handling tasks
    handlers = {'open': handler_tasks.handle_open_event}

    # url provided on webhook creation at Mandrill
    # NGROK setting must be replaced with production setting
    url = settings.NGROK_HOST + '/hooks/'

    # authentication key (Mandrill)
    webhooks_key = settings.WEBHOOKS_KEY

    def __init__(self, payload, signature):
        '''Checks authenticity and dispatches tasks for Celery
        
        :payload: event payload
        :signature: Mandrill webhook signature
            '''
        self.payload = payload
        if self._signed(signature):
            self.payload = json.loads(payload['mandrill_events'])
            self._dispatch()

    def _dispatch(self):
        '''Method triggers custom handler Celery tasks
        if handler for specific event is not provided -
        triggers '.tasks.handler_tasks.handle_default_event'
        '''
        for event in self.payload:
            try:
                if event['event'] in self.handlers.keys():
                    handler_task = self.handlers[event['event']]
                else:
                    handler_task = handler_tasks.handle_default_event
                # Celery task call
                handler_task.delay(event)
            except KeyError:
                # unhandled keys. e.g. Mandrill 'actions'
                pass

    def _signed(self, signature):
        '''Checks authenticity of Mandrill webhook payload

        :signature: request META parameter HTTP_X_MANDRILL_SIGNATURE
        '''
        signed_data = self.url
        for key, value in sorted(self.payload.items()):
            signed_data += key + value
        
        hashed = hmac.new(self.webhooks_key,
                        msg=signed_data.encode('utf-8'),
                        digestmod=hashlib.sha1).digest()
        decoded = base64.b64encode(hashed).decode()
        return decoded == signature