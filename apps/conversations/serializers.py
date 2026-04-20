"""Serializers para la API de conversaciones."""

from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Message.

    Serializa los campos: id, role, content, created_at, tokens_used.
    """

    class Meta:
        model = Message
        fields = ["id", "role", "content", "created_at", "tokens_used"]
        read_only_fields = ["id", "created_at", "tokens_used"]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Conversation.

    Serializa los campos: id, title, model, created_at, updated_at, messages.
    """

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "title", "model",
                  "created_at", "updated_at", "messages"]
        read_only_fields = ["id", "created_at", "updated_at"]


class SendMessageSerializer(serializers.Serializer):
    """Serializer para enviar mensajes a la API.

    Campos:
        content: Contenido del mensaje (requerido).
        model: Modelo de IA a usar (opcional).
    """

    content = serializers.CharField(required=True, min_length=1)
    model = serializers.CharField(required=False, allow_blank=True)
