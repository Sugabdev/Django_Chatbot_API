"""Servicios para la integración con OpenRouter."""

from apps.conversations.models import Message


def build_message_history(conversation_id) -> list[dict]:
    """Construir historial de mensajes para OpenRouter.

    Args:
        conversation_id: UUID de la conversación.

    Returns:
        List of dict: Lista de mensajes en formato OpenAI.
    """
    messages = Message.objects.filter(conversation_id=conversation_id).order_by(
        "created_at"
    )

    history = []
    for msg in messages:
        history.append(
            {
                "role": msg.role,
                "content": msg.content,
            }
        )

    return history
