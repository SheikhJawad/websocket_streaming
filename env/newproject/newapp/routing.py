# newapp/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/stream/', consumers.VideoStreamConsumer.as_asgi()),
    
]
