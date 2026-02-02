import requests
import json
from src.llm.provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):

    def __init__(self, model: str, base_url: str):
        self.model = model
        self.base_url = base_url

    def invoke(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
