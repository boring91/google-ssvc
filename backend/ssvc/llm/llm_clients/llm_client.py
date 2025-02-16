import logging
from abc import abstractmethod

from ssvc.llm.utils import parse_llm_response


class LlmClient:
    _instance = None

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def respond(self, query: str) -> str:
        return self._get_evaluated_response(query)

    def _get_evaluated_response(self, query: str) -> str:
        # 1. Ask the original query
        response = self._respond_with_retry(query)
        if response is None:
            return ''

        # 2. Ask for evaluation
        evaluation_query = f"""You are a question-answer evaluator. I'll give you a query provided by user A and the 
        response provided by user B. Your role is to evaluate the correctness and accuracy of the provided response
        to the query. Your evaluation should be provided as a json object. The json object should contain two 
        properties: `score` that takes a value between 0 and 1; 0 being user B's response provided to user A's query 
        does not answer the their query and 1 being the query of user A has been answered by the user B's response 
        accurately; and the second property is `justification`; which is a description of why the that specific `score` 
        was given to the query-response pair. This justification would be given back to user B who provided the 
        response to user A's query to adjust their answer based on it if the evaluation score is low.
        
        You should only respond with the json object nothing more; i.e., starts with ```json.
        
        QUERY: {query}
        RESPONSE: {response}
        """

        evaluation_response = self._respond_with_retry(evaluation_query)

        if evaluation_response is None:
            return ''

        evaluation_response = parse_llm_response(evaluation_response, False)

        # 3.1. If pass evaluation, return the response.
        if evaluation_response['score'] >= 0.95:
            return response

        # 3.2. If didn't pass the evaluation, ask the original query and
        # provide the evaluation for correction.
        self._logger.info('The provided llm answer did not pass evaluation score threshold, asking again...')
        reevaluated_query = f"""You are user B who provided the response to the scenario below:
        {evaluation_query}
        
        I want you to provide a new response based on the evaluation justification below:
        {evaluation_response['justification']}
        
        Again, the format of your response should be the same as your original response.
        """

        return self._respond_with_retry(reevaluated_query)

    def _respond_with_retry(self, query: str) -> str:
        def run_process() -> str:
            # noinspection PyBroadException
            try:
                return self._process(query)

            except:
                self._logger.warning(f'Could not find a proper response to query: {query}.')
                return ''

        result = run_process()

        # If no result was returned from the llm,
        # we ask it again.
        if result is None or result == '':
            return run_process()

        return result

    @abstractmethod
    def _process(self, query: str) -> str:
        pass
