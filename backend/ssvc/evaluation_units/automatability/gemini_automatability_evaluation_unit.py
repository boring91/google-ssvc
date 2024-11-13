from typing import Optional

from ssvc.evaluation_units.automatability.base_automatability_evaluation_unit import BaseAutomatabilityEvaluationUnit
from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.llm.llm_evaluators.automatability_llm_evaluator import AutomatabilityLlmEvaluator


class GeminiAutomatabilityEvaluationUnit(BaseAutomatabilityEvaluationUnit):
    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        llm_evaluator = AutomatabilityLlmEvaluator('gemini')
        result = llm_evaluator.evaluate(cve_id, reevaluate)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'], result['links'])
