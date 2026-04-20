from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "model", "created_at", "updated_at"]
    search_fields = ["title"]
    ordering = ["-updated_at"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "conversation", "role", "content", "created_at"]
    list_filter = ["role", "created_at"]
    ordering = ["created_at"]
