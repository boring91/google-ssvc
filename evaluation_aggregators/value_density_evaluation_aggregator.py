from typing import List, Literal

from evaluation_aggregators.base_evaluation_aggregator import BaseEvaluationAggregator
from evaluation_units.evaluation_unit import EvaluationUnit
from evaluation_units.value_density.base_value_density_evaluation_unit import BaseValueDensityEvaluationUnit
from evaluation_units.value_density.gemini_value_density_evaluation_unit import GeminiValueDensityEvaluationUnit
from evaluation_units.value_density.heuristic_value_density_evaluation_unit import HeuristicValueDensityEvaluationUnit
from evaluation_units.value_density.openai_value_density_evaluation_unit import OpenaiValueDensityEvaluationUnit


class ValueDensityEvaluationAggregator(BaseEvaluationAggregator):
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        super().__init__(llm)
        self._units: List[BaseValueDensityEvaluationUnit] = [
            HeuristicValueDensityEvaluationUnit(),
            GeminiValueDensityEvaluationUnit() if llm == 'gemini' else OpenaiValueDensityEvaluationUnit()
        ]

    def _get_units(self) -> List[EvaluationUnit]:
        return self._units
