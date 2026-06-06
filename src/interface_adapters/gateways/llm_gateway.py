from abc import ABC, abstractmethod


class LlmGatewayInterface(ABC):
    @abstractmethod
    async def send(self, prompt: str) -> str:
        pass
