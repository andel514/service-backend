import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import OrderChatRoom, OrderMessage, ExecutorChatRoom, ExecutorMessage

class OrderChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'order_chat_{self.room_id}'
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        msg = await self.save_message(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': msg.timestamp.isoformat(),
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
    
    @database_sync_to_async
    def save_message(self, content):
        room = OrderChatRoom.objects.get(id=self.room_id)
        return OrderMessage.objects.create(room=room, sender=self.user, content=content)

class ExecutorChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'executor_chat_{self.room_id}'
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return
        has_access = await self.check_access()
        if not has_access:
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    @database_sync_to_async
    def check_access(self):
        room = ExecutorChatRoom.objects.get(id=self.room_id)
        return self.user in room.participants.all() and self.user not in room.blocked_users.all()
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        if await self.is_blocked():
            return
        msg = await self.save_message(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': msg.timestamp.isoformat(),
                'id': msg.id,
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
    
    @database_sync_to_async
    def is_blocked(self):
        room = ExecutorChatRoom.objects.get(id=self.room_id)
        return self.user in room.blocked_users.all()
    
    @database_sync_to_async
    def save_message(self, content):
        room = ExecutorChatRoom.objects.get(id=self.room_id)
        return ExecutorMessage.objects.create(room=room, sender=self.user, content=content)