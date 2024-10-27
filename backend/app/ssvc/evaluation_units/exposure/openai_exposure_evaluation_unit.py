from typing import Optional, Literal

from app.ssvc.evaluation_units.evaluation_unit import EvaluationResult
from app.ssvc.evaluation_units.exposure.base_exposure_evaluation_unit import BaseExposureEvaluationUnit
from app.ssvc.llm.llm_evaluators.exposure_llm_evaluator import ExposureLlmEvaluator


class OpenaiExposureEvaluationUnit(BaseExposureEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[EvaluationResult[Literal['open', 'small', 'controlled']]]:
        llm_evaluator = ExposureLlmEvaluator('openai')
        result = llm_evaluator.evaluate(cve_id)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
