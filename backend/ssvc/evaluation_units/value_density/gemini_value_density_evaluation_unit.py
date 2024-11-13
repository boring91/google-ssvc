from typing import Optional

from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.value_density.base_value_density_evaluation_unit import BaseValueDensityEvaluationUnit
from ssvc.llm.llm_evaluators.value_density_llm_evaluator import ValueDensityLlmEvaluator


class GeminiValueDensityEvaluationUnit(BaseValueDensityEvaluationUnit):
    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        llm_evaluator = ValueDensityLlmEvaluator('gemini')
        result = llm_evaluator.evaluate(cve_id, reevaluate)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'], result['links'])
