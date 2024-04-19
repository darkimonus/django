from django.urls import path
from chats.views import private_chat_view, chat_main_view

app_name = 'chats'

urlpatterns = [
    path('', chat_main_view, name='main'),
    path('<int:user_id>/', private_chat_view, name='private-chat'),
]
