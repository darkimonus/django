from django.urls import path, re_path
from chats.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path('ws/chats/<str:room_name>/', ChatConsumer.as_asgi()),
]
