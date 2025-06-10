from google import genai
from google.genai import types

from ssvc.llm.llm_clients.llm_client import LlmClient


class GeminiLlmClient(LlmClient):
    def __init__(self):
        super().__init__()

        self._generation_config = {
            "max_output_tokens": 8192,
            "temperature": 0.2,
            "top_p": 0.95,
        }

        self._safety_settings = types.GenerateContentConfig(
            temperature=1,
            top_p=1,
            seed=0,
            max_output_tokens=65535,
            safety_settings=[types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ), types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )],
        )

        self._client = genai.Client(
            vertexai=True,
            project="sw-supply-chain-sec-dev-1184",
            location="global",
        )

    def _process(self, query: str) -> str:
        response = self._client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=query)
                    ]
                ),
            ],
            config=self._safety_settings
        )

        return response.text


gemini_llm_client = GeminiLlmClient()
