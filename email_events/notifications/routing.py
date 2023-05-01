'''Channels routing'''
from django.urls import re_path
from notifications import consumers


websocket_urlpatterns = [
    re_path(r"", consumers.OpenEventConsumer.as_asgi()),
]