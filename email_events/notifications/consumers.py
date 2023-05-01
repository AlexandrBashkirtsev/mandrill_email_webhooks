'''Channels consumer classes'''
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class OpenEventConsumer(WebsocketConsumer):
    '''Open event handling websocket.
    Connects to channels layer with :open_event: group
    and accept client connection.'''
    def connect(self):        
        self.event_group_name = 'open_event'
        async_to_sync(self.channel_layer.group_add)(self.event_group_name, self.channel_name)
        self.accept()
    
    def disconnect(self, code):
        '''Closes group connection on closing websocket'''
        async_to_sync(self.channel_layer.group_discard)(
            self.event_group_name, self.channel_name
        )

    def send_new_event(self, context):
        '''Sends event to websocket client.
        
        :context: event payload serialized dictionary.
        '''
        self.send(json.dumps(context))