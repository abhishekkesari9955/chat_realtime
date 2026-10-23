
from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "is_group", "created_at")
    search_fields = ("name", "description", "created_by__username")
    filter_horizontal = ("members",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("room", "sender", "created_at")
    search_fields = ("content", "sender__username", "room__name")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "edited_at")
