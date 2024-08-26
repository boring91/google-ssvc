from abc import abstractmethod


class LlmClient:

    @abstractmethod
    def respond(self, query) -> str:
        pass
