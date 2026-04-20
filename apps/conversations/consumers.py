import json
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.conf import settings
from apps.conversations.models import Conversation, Message
from apps.ai.client import OpenRouterClient
from apps.ai.services import build_message_history


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            conversation_id = data.get("conversation_id")
            content = data.get("content")
            model = data.get("model", settings.DEFAULT_MODEL)

            if not conversation_id or not content:
                await self.send(
                    json.dumps(
                        {
                            "type": "error",
                            "detail": "conversation_id and content are required",
                        }
                    )
                )
                return

            conversation = await self.get_conversation(conversation_id)
            if not conversation:
                await self.send(
                    json.dumps(
                        {"type": "error", "detail": "Conversation not found"})
                )
                return

            user_message = await self.create_message(conversation, "user", content)

            history = build_message_history(conversation_id)
            history.append({"role": "user", "content": content})

            client = OpenRouterClient()
            full_response = ""

            async for token in client.chat_completion_stream(history, model=model):
                full_response += token
                await self.send(json.dumps({"type": "token", "content": token}))

            assistant_message = await self.create_message(
                conversation, "assistant", full_response
            )

            await self.send(
                json.dumps(
                    {"type": "done", "message_id": str(assistant_message.id)})
            )

        except json.JSONDecodeError:
            await self.send(json.dumps({"type": "error", "detail": "Invalid JSON"}))
        except Exception as e:
            await self.send(json.dumps({"type": "error", "detail": str(e)}))

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, conversation, role, content):
        return Message.objects.create(
            conversation=conversation, role=role, content=content
        )
