import logging
from abc import abstractmethod


class LlmClient:
    _instance = None

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def respond(self, query: str) -> str:
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
