from abc import abstractmethod
from typing import Optional, Literal, List

from evaluation_units.evaluation_unit import EvaluationResult, EvaluationUnit


class BaseEvaluationAggregator():
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        pass

    @abstractmethod
    def _get_units(self) -> List[EvaluationUnit]:
        pass

    def aggregate(self, cve_id: str) -> Optional[EvaluationResult]:
        for unit in self._get_units():
            result = unit.evaluate(cve_id)
            if result is not None:
                return result

        return None
