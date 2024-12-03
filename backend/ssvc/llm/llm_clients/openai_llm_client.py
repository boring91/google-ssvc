import os
from openai import OpenAI

from ssvc.llm.llm_clients.llm_client import LlmClient


class OpenaiLlmClient(LlmClient):

    def __init__(self):
        super().__init__()

        self._client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def _process(self, query: str) -> str:
        completion = self._client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": query}
            ],
            temperature=0
        )

        return completion.choices[0].message.content
