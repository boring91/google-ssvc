import vertexai
from vertexai.generative_models import SafetySetting, GenerativeModel

from llm.llm_clients.llm_client import LlmClient


class GeminiLlmClient(LlmClient):
    def __init__(self):
        self._generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }

        self._safety_settings = [
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
            )
        ]

        vertexai.init(project="sw-supply-chain-sec-dev-1184", location="australia-southeast1")
        self._model = GenerativeModel("gemini-1.5-pro-001")

    def respond(self, query) -> str:
        responses = self._model.generate_content(
            query,
            generation_config=self._generation_config,
            safety_settings=self._safety_settings,
            stream=True)

        answer_parts = []

        for response in responses:
            answer_parts.append(response.text)

        answer = ''.join(answer_parts)

        return answer


gemini_llm_client = GeminiLlmClient()
