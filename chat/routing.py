
from django.urls import path

from .consumers import ChatConsumer


websocket_urlpatterns = [
    path(
        "ws/chat/rooms/<int:room_id>/",
        ChatConsumer.as_asgi(),
        name="chat_websocket",
    ),
]
