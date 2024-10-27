from typing import List, Literal

from ssvc.evaluation_aggregators.base_evaluation_aggregator import BaseEvaluationAggregator
from ssvc.evaluation_units.evaluation_unit import EvaluationUnit
from ssvc.evaluation_units.technical_impact.base_technical_impact_evaluation_unit import BaseTechnicalImpactEvaluationUnit
from ssvc.evaluation_units.technical_impact.gemini_technical_impact_evaluation_unit import \
    GeminiTechnicalImpactEvaluationUnit
from ssvc.evaluation_units.technical_impact.openai_technical_impact_evaluation_unit import \
    OpenaiTechnicalImpactEvaluationUnit
from ssvc.evaluation_units.technical_impact.vulnrichment_technical_impact_evaluation_unit import \
    VulnrichmentTechnicalImpactEvaluationUnit


class TechnicalImpactEvaluationAggregator(BaseEvaluationAggregator):
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        super().__init__(llm)
        self._units: List[BaseTechnicalImpactEvaluationUnit] = [
            VulnrichmentTechnicalImpactEvaluationUnit(),
            GeminiTechnicalImpactEvaluationUnit() if llm == 'gemini' else OpenaiTechnicalImpactEvaluationUnit()
        ]

    def _get_units(self) -> List[EvaluationUnit]:
        return self._units
