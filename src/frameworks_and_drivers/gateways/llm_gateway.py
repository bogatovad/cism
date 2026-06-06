import httpx

from src.frameworks_and_drivers.gateways.settings import openrouter_settings
from src.interface_adapters.gateways.llm_gateway import LlmGatewayInterface

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterLlmGateway(LlmGatewayInterface):
    async def send(self, prompt: str) -> str:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OPENROUTER_CHAT_URL,
                headers={
                    "Authorization": f"Bearer {openrouter_settings.api_key}",
                    "HTTP-Referer": openrouter_settings.site_url,
                    "X-OpenRouter-Title": openrouter_settings.site_name,
                },
                json={
                    "model": openrouter_settings.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                },
            )
            response.raise_for_status()
            data = response.json()

        choices = data.get("choices") or []

        if not choices:
            raise ValueError("OpenRouter returned empty choices")

        message = choices[0].get("message") or {}
        content = message.get("content")

        if not content:
            raise ValueError("OpenRouter returned empty content")

        return content
