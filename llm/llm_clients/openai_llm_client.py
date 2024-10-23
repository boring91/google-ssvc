import os
from openai import OpenAI

from llm.llm_clients.llm_client import LlmClient


class OpenaiLlmClient(LlmClient):

    def __init__(self):
        self._client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def respond(self, query) -> str:
        completion = self._client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": query}
            ]
        )

        return completion.choices[0].message.content
