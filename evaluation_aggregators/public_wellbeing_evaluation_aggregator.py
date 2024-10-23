from typing import List, Literal

from evaluation_aggregators.base_evaluation_aggregator import BaseEvaluationAggregator
from evaluation_units.evaluation_unit import EvaluationUnit
from evaluation_units.public_wellbeing.base_public_wellbeing_evaluation_unit import BasePublicWellbeingEvaluationUnit
from evaluation_units.public_wellbeing.gemini_public_wellbeing_evaluation_unit import \
    GeminiPublicWellbeingEvaluationUnit
from evaluation_units.public_wellbeing.openai_public_wellbeing_evaluation_unit import \
    OpenaiPublicWellbeingEvaluationUnit


class PublicWellbeingEvaluationAggregator(BaseEvaluationAggregator):
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        super().__init__(llm)
        self._units: List[BasePublicWellbeingEvaluationUnit] = [
            GeminiPublicWellbeingEvaluationUnit() if llm == 'gemini' else OpenaiPublicWellbeingEvaluationUnit()
        ]

    def _get_units(self) -> List[EvaluationUnit]:
        return self._units
