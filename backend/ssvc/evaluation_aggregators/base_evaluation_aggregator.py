from abc import abstractmethod
from typing import Optional, Literal, List

from ssvc.evaluation_units.evaluation_unit import EvaluationResult, EvaluationUnit


class BaseEvaluationAggregator:
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        pass

    @abstractmethod
    def _get_units(self) -> List[EvaluationUnit]:
        pass

    def aggregate(self, cve_id: str, reevaluate: bool = False) -> Optional[EvaluationResult]:
        for unit in self._get_units():
            result = unit.evaluate(cve_id, reevaluate)
            if result is not None:
                return result

        return None
