import json
import re
from abc import abstractmethod
from typing import Literal, Optional

from cve_data_source_aggregator import CveDataSourceAggregator
from gemini_llm_client import GeminiLlmClient
from llm_client import LlmClient
from openai_llm_client import OpenAiLlmClient


class BaseEvaluator:
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        self._llm_client: LlmClient = GeminiLlmClient() if llm == 'gemini' else OpenAiLlmClient()
        self._cve_data_source_aggregator = CveDataSourceAggregator()

    def evaluate(self, cve_id) -> Optional[dict]:
        cve_data = self._get_cve_data(cve_id)

        query = self._get_prompt(cve_id, cve_data)
        llm_response = self._llm_client.respond(query)

        return _parse_llm_response(llm_response)

    @abstractmethod
    def _get_prompt(self, cve_id: str, cve_data: str) -> str:
        pass

    def _get_cve_data(self, cve_id) -> str:
        cve_data = self._cve_data_source_aggregator.load(cve_id)
        return json.dumps(cve_data)


def _parse_llm_response(llm_response: str) -> Optional[dict]:
    cleaned = llm_response.replace('\n', '').replace('\t', '')
    pattern = r'```json(\{.+?\})```'
    match = re.search(pattern, cleaned)

    if match:
        captured_group = match.group(1)
        result: dict = json.loads(captured_group)

        if 'assessment' in result:
            return result

        else:
            return None

    else:
        return None
