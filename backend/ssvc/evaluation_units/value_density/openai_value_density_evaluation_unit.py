from typing import Optional, Literal

from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.value_density.base_value_density_evaluation_unit import BaseValueDensityEvaluationUnit
from ssvc.llm.llm_evaluators.value_density_llm_evaluator import ValueDensityLlmEvaluator


class OpenaiValueDensityEvaluationUnit(BaseValueDensityEvaluationUnit):
    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        llm_evaluator = ValueDensityLlmEvaluator('openai')
        result = llm_evaluator.evaluate(cve_id, reevaluate)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
