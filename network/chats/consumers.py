import json
from channels.generic.websocket import AsyncWebsocketConsumer
import aioredis
from datetime import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Join room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

        # Retrieve messages from Redis and send them to WebSocket only once during connection
        if not hasattr(self, 'messages_loaded'):
            redis = aioredis.from_url('redis://localhost:6380')
            messages = await redis.lrange(self.room_name, 0, -1)
            for message in messages:
                await self.send(text_data=message.decode('utf-8'))
            self.messages_loaded = True

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        message_data = {
            'message': message,
            'sender': self.user_id,
            'timestamp': datetime.now().isoformat()
        }

        # Save message to Redis
        redis = aioredis.from_url('redis://localhost:6380')
        await redis.rpush(self.room_name, json.dumps(message_data))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user_id,
                'timestamp': message_data['timestamp']
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))
