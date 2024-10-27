from typing import List, Literal

from app.ssvc.evaluation_aggregators.base_evaluation_aggregator import BaseEvaluationAggregator
from app.ssvc.evaluation_units.evaluation_unit import EvaluationUnit
from app.ssvc.evaluation_units.exposure.base_exposure_evaluation_unit import BaseExposureEvaluationUnit
from app.ssvc.evaluation_units.exposure.gemini_exposure_evaluation_unit import GeminiExposureEvaluationUnit
from app.ssvc.evaluation_units.exposure.heuristic_exposure_evaluation_unit import HeuristicExposureEvaluationUnit
from app.ssvc.evaluation_units.exposure.openai_exposure_evaluation_unit import OpenaiExposureEvaluationUnit


class ExposureEvaluationAggregator(BaseEvaluationAggregator):
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        super().__init__(llm)
        self._units: List[BaseExposureEvaluationUnit] = [
            HeuristicExposureEvaluationUnit(),
            GeminiExposureEvaluationUnit() if llm == 'gemini' else OpenaiExposureEvaluationUnit()
        ]

    def _get_units(self) -> List[EvaluationUnit]:
        return self._units
