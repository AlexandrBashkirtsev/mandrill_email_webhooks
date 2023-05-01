from emailhooks import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class EventHandler:
    '''Base class EventHandlers provides common functionality
    for handling events.
    '''
    def __init__(self, payload):
        self.payload = payload

    def create_event(self, model):
        '''Creates Django model object instance and updates it with payload'''
        self.event = model()
        self.event.__dict__.update(self.payload)

    def save_event(self):
        """Validates and saves event model instance"""
        self.event.full_clean()
        self.event.save()

    def handle(self):
        '''Provides procedure of event-depending handling.
        Saves payload to permanent storage.'''
        self.create_event()
        self.save_event()


class DefaultEventHadler(EventHandler):
    '''DefaultEventHandler connects to DefaultEvent Django model.
    No special handling provided.
    '''
    model = models.DefaultEvent
    
    def create_event(self):
        super().create_event(model=self.model)


class OpenEventHandler(EventHandler):
    '''OpenEventHandler connects to OpenEvent Django model.
    Provides additional steps for handling 'open' Mandrill webhook events'''
    model = models.OpenEvent
    msg_model = models.OpenMessage

    def create_event(self):
        '''Serializes additional layer of event payload - 'msg'
        and saves it to permanent storage.
        '''
        super().create_event(model=self.model)
        msg = self.msg_model()
        self.msg_payload = self.payload['msg']
        msg.__dict__.update(self.msg_payload)
        msg.full_clean()
        msg.save()
        self.event.msg = msg

    def handle(self):
        '''Handling procedure of 'open' event.
        In addition to default handling - uploads event payload to
        :channels: layer [Redis] in 'opesn_event' group.
        Then saves payload to permanent storage.
        '''
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'open_event',
            {
                'type': 'send_new_event',
                'context': self.payload,
            },
        )
        self.create_event()
        self.save_event()
