from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from django.conf import settings

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    SendMessageSerializer,
)
from apps.ai.client import OpenRouterClient
from apps.ai.services import build_message_history


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar conversaciones.

    Proporciona endpoints para listar, crear, obtener,
    actualizar y eliminar conversaciones.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """Obtiene el queryset de conversaciones."""
        return Conversation.objects.all()

    def create(self, request, *args, **kwargs):
        """Crea una nueva conversación.

        Args:
            request: Request con datos opcionales 'model'.

        Returns:
            Response: Conversación creada con estado 201.
        """
        model = request.data.get("model", settings.DEFAULT_MODEL)
        conversation = Conversation.objects.create(
            user=None,
            title=None,
            model=model,
        )
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Elimina una conversación.

        Args:
            request: Request con la conversación a eliminar.

        Returns:
            Response: Estado 204 sin contenido.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def messages(self, request, pk=None):
        """Envía un mensaje y recibe respuesta de la IA.

        Args:
            request: Request con 'content' (requerido) y 'model' (opcional).
            pk: ID de la conversación.

        Returns:
            Response: Diccionario con mensaje del usuario y del asistente.
        """
        conversation = self.get_object()

        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_content = serializer.validated_data["content"]
        model = serializer.validated_data.get("model") or conversation.model

        user_message = Message.objects.create(
            conversation=conversation,
            role="user",
            content=user_content,
        )

        history = build_message_history(conversation.id)

        client = OpenRouterClient()

        import asyncio

        async def get_response():
            return await client.chat_completion(history, model=model)

        assistant_content = asyncio.run(get_response())

        assistant_message = Message.objects.create(
            conversation=conversation,
            role="assistant",
            content=assistant_content,
        )

        return Response(
            {
                "user_message": MessageSerializer(user_message).data,
                "assistant_message": MessageSerializer(assistant_message).data,
            },
            status=status.HTTP_200_OK,
        )
