
from django import forms

from .models import ChatRoom, Message


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ("name", "description")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter room name",
                    "maxlength": 100,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "What is this room about?",
                    "rows": 3,
                    "maxlength": 255,
                }
            ),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("content",)

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Type your message...",
                    "rows": 3,
                    "maxlength": 5000,
                }
            ),
        }
