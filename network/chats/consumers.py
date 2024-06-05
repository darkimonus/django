import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6380, db=0)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Отримати попередні повідомлення з Redis і відправити їх користувачу
        previous_messages = redis_client.lrange(self.room_group_name, 0, -1)
        for message in previous_messages:
            await self.send(text_data=message.decode('utf-8'))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Зберегти повідомлення в Redis
        await redis_client.rpush(self.room_group_name, json.dumps({
            'message': message
        }))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
