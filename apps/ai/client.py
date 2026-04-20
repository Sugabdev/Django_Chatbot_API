"""Cliente para interacting with OpenRouter API."""

import os
from typing import AsyncGenerator, Optional

import httpx
from openai import AsyncOpenAI

from django.conf import settings

from .exceptions import (
    OpenRouterError,
    OpenRouterTimeoutError,
    OpenRouterAuthenticationError,
    OpenRouterRateLimitError,
    OpenRouterInvalidRequestError,
)


class OpenRouterClient:
    """Client for interacting with OpenRouter API.

    Provides methods for complete and streaming chat completions
    using OpenAI-compatible SDK with OpenRouter backend.

    Attributes:
        api_key: OpenRouter API key.
        base_url: OpenRouter API base URL.
        default_model: Default model identifier.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None,
    ):
        """Initialize OpenRouter client.

        Args:
            api_key: OpenRouter API key. Uses settings if not provided.
            base_url: Base URL for API. Uses settings if not provided.
            default_model: Default model to use. Uses settings if not provided.
        """
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.base_url = base_url or settings.OPENROUTER_BASE_URL
        self.default_model = default_model or settings.DEFAULT_MODEL
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            http_client=httpx.AsyncClient(timeout=120.0),
        )

    async def chat_completion(
        self,
        messages: list[dict],
        model: Optional[str] = None,
    ) -> str:
        """Send a chat completion request.

        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            model: Model identifier. Uses default if not provided.

        Returns:
            str: Assistant's response content.

        Raises:
            OpenRouterTimeoutError: If request times out.
            OpenRouterAuthenticationError: If API key is invalid.
            OpenRouterRateLimitError: If rate limit exceeded.
            OpenRouterError: For other HTTP errors.
        """
        model = model or self.default_model

        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content or ""
        except httpx.TimeoutException as e:
            raise OpenRouterTimeoutError(f"Timeout: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise OpenRouterAuthenticationError(
                    f"Authentication failed: {e}")
            if e.response.status_code == 429:
                raise OpenRouterRateLimitError(f"Rate limit exceeded: {e}")
            raise OpenRouterError(f"HTTP error: {e}")
        except Exception as e:
            raise OpenRouterError(f"Unexpected error: {e}")

    async def chat_completion_stream(
        self,
        messages: list[dict],
        model: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """Send a streaming chat completion request.

        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            model: Model identifier. Uses default if not provided.

        Yields:
            str: Individual tokens from the streaming response.

        Raises:
            OpenRouterTimeoutError: If request times out.
            OpenRouterAuthenticationError: If API key is invalid.
            OpenRouterRateLimitError: If rate limit exceeded.
            OpenRouterError: For other HTTP errors.
        """
        model = model or self.default_model

        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except httpx.TimeoutException as e:
            raise OpenRouterTimeoutError(f"Timeout: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise OpenRouterAuthenticationError(
                    f"Authentication failed: {e}")
            if e.response.status_code == 429:
                raise OpenRouterRateLimitError(f"Rate limit exceeded: {e}")
            raise OpenRouterError(f"HTTP error: {e}")
        except Exception as e:
            raise OpenRouterError(f"Unexpected error: {e}")
