
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import ChatRoom, Message


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_room_{self.room_id}"

        if not user.is_authenticated:
            await self.close(code=4401)
            return

        is_member = await self.check_room_membership(
            self.room_id,
            user.pk,
        )

        if not is_member:
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, TypeError):
            return
        
        event_type = data.get("type", "message")
        user = self.scope["user"]

        if event_type == "typing":
            is_typing = data.get("is_typing")

            if not isinstance(is_typing, bool):
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing.status",
                    "sender_id": user.pk,
                    "sender": user.display_name or user.username,
                    "is_typing": is_typing,
                },
            )
            return

        if event_type != "message":
            return

        content = data.get("content", "")

        if not isinstance(content, str):
            return

        content = content.strip()

        if not content or len(content) > 5000:
            return

        user = self.scope["user"]

        message_data = await self.save_message(
            self.room_id,
            user.pk,
            content,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_data,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "type": "chat_message",
                "message": event["message"],
            })
        )
    
    async def typing_status(self, event):
        await self.send(
            text_data=json.dumps({
                "type": "typing_status",
                "sender_id": event["sender_id"],
                "sender": event["sender"],
                "is_typing": event["is_typing"],
            })
        )

    @database_sync_to_async
    def check_room_membership(self, room_id, user_id):
        return ChatRoom.objects.filter(
            pk=room_id,
            members__pk=user_id,
        ).exists()

    @database_sync_to_async
    def save_message(self, room_id, user_id, content):
        room = ChatRoom.objects.get(pk=room_id)
        user = User.objects.get(pk=user_id)

        message = Message.objects.create(
            room=room,
            sender=user,
            content=content,
        )

        return {
            "sender_id": user.pk,
            "id": message.pk,
            "content": message.content,
            "sender": user.display_name or user.username,
            "created_at": message.created_at.strftime("%d %b %Y, %H:%M"),
        }
