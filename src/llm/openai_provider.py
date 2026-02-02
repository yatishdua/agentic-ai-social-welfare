import os
from openai import OpenAI
from src.llm.provider import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):

    def __init__(self, model: str, temperature: float = 0):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": "You are a JSON-only extraction engine."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
