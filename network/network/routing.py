from django.urls import path
from chats.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chats/<str:room_name>/', ChatConsumer.as_asgi()),
]
