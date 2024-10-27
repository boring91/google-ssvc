from typing import Optional, Literal

from evaluation_units.evaluation_unit import EvaluationResult
from evaluation_units.exposure.base_exposure_evaluation_unit import BaseExposureEvaluationUnit
from llm.llm_evaluators.exposure_llm_evaluator import ExposureLlmEvaluator


class GeminiExposureEvaluationUnit(BaseExposureEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[EvaluationResult[Literal['open', 'small', 'controlled']]]:
        llm_evaluator = ExposureLlmEvaluator('gemini')
        result = llm_evaluator.evaluate(cve_id)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
