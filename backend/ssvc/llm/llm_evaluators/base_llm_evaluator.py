import json
import logging
import re
from abc import abstractmethod
from typing import Literal, Optional

from app.data_sources.cve_data_source_aggregator import CveDataSourceAggregator
from database.db import Db
from ssvc.llm.llm_clients.gemini_llm_client import GeminiLlmClient
from ssvc.llm.llm_clients.llm_client import LlmClient
from ssvc.llm.llm_clients.openai_llm_client import OpenaiLlmClient


class BaseLlmEvaluator:
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        self._name = self.__class__.name()
        self._llm = llm
        self._llm_client: LlmClient = GeminiLlmClient() if llm == 'gemini' else OpenaiLlmClient()
        self._cve_data_source_aggregator = CveDataSourceAggregator()

    def evaluate(self, cve_id: str, reevaluate: bool = False) -> Optional[dict]:
        cve_id = cve_id.upper()

        if not reevaluate:
            with Db() as db:
                cached_data = db.first(
                    'SELECT * FROM llm_evaluator_cache WHERE llm = %s AND cve_id = %s AND decision_point = %s',
                    (self._llm, cve_id, self._name))

            if cached_data is not None:
                return json.loads(cached_data['data'])

            logging.info(f'No cached evaluation was found for cve {cve_id}, running llm evaluator.')

        else:
            with Db() as db:
                db.execute('DELETE FROM llm_evaluator_cache WHERE llm = %s AND cve_id = %s AND decision_point = %s',
                           (self._llm, cve_id, self._name))

        cve_data = self._get_cve_data(cve_id)

        query = self._get_prompt(cve_id, cve_data)

        try:
            llm_response = self._llm_client.respond(query)
        except:
            return None

        parsed_response = _parse_llm_response(llm_response)

        if parsed_response is None:
            return None

        # Cache the response
        with Db() as db:
            db.execute(
                """
                INSERT INTO llm_evaluator_cache(llm, cve_id, decision_point, data) VALUES (%s, %s, %s, %s)
                ON CONFLICT (llm, cve_id, decision_point) DO NOTHING;
                """,
                (self._llm, cve_id, self._name, json.dumps(parsed_response)))

        return parsed_response

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    def _get_question(self) -> str:
        pass

    @abstractmethod
    def _get_description(self) -> str:
        pass

    def _get_prompt(self, cve_id: str, cve_data: str) -> str:
        return f"""I am going to give you an ID of a specific ID and some data related to that CVE in a json format. The 
        json object has at its roots properties that represent different data sources, each property of these is 
        assigned to another json object that represent the information about the given CVE from that data source. Your 
        role is to use the provided information from these data sources and answer the following question:
        
        {self._get_question()}
        
        {self._get_description()}
        
        You answer should be formatted as a json object with two properties: 1) "cve_id" which contains the id of the 
        cve in question, 2) "assessment" which holds your final assessment of the CVE, 3) "justification": explaining 
        how you reached to the answer you provided in the "assessment" property (the description should not refer to the 
        json data but rather talks about the information that led you to this conclusion, aka, avoid saying the json 
        data shows etc. Also avoid giving generic descriptions like: "multiple sources have reported etc." but rather 
        provide concrete descriptions: e.g., name the sources, name the versions or software, provide links if 
        available, etc. In addition the style of the assessment should be passive for instance, rather than saying "I am
        unable to find any information about this vulnerability", you should say "No information was found about this 
        vulnerability", you do not have to use those exact same words but you should not use "I"), 
        and 4) "confidence": ranges between 0 and 1, which indicates how confident you are in your 
        assessment, 1 being very confident.

        You should only respond with the json object nothing more.

        Here are the two pieces of information:

        CVE ID: {cve_id}
        JSON data: {cve_data}
        """

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
