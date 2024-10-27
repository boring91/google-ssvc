from typing import List, Literal

from ssvc.evaluation_aggregators.base_evaluation_aggregator import BaseEvaluationAggregator
from ssvc.evaluation_units.automatability.base_automatability_evaluation_unit import BaseAutomatabilityEvaluationUnit
from ssvc.evaluation_units.automatability.gemini_automatability_evaluation_unit import GeminiAutomatabilityEvaluationUnit
from ssvc.evaluation_units.automatability.openai_automatability_evaluation_unit import OpenaiAutomatabilityEvaluationUnit
from ssvc.evaluation_units.automatability.vulnrichment_automatability_evaluation_unit import \
    VulnrichmentAutomatabilityEvaluationUnit
from ssvc.evaluation_units.evaluation_unit import EvaluationUnit


class AutomatabilityEvaluationAggregator(BaseEvaluationAggregator):
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        super().__init__(llm)
        self._units: List[BaseAutomatabilityEvaluationUnit] = [
            VulnrichmentAutomatabilityEvaluationUnit(),
            GeminiAutomatabilityEvaluationUnit() if llm == 'gemini' else OpenaiAutomatabilityEvaluationUnit()
        ]

    def _get_units(self) -> List[EvaluationUnit]:
        return self._units
