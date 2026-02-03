import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatUser, Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        username = data["username"]
        phone = data["phone"]
        message = data["message"]

        user = await self.get_or_create_user(username, phone)
        msg = await self.save_message(user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": user.username,
                "message": msg.content,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_or_create_user(self, username, phone):
        user, created = ChatUser.objects.get_or_create(
            username=username,
            defaults={"phone": phone}
        )
        return user

    @database_sync_to_async
    def save_message(self, user, message):
        return Message.objects.create(
            room=self.room_name,
            user=user,
            content=message
        )
