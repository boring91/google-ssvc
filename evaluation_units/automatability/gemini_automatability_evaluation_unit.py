from typing import Optional, Literal

from evaluation_units.automatability.base_automatability_evaluation_unit import BaseAutomatabilityEvaluationUnit
from evaluation_units.evaluation_unit import EvaluationResult
from llm.llm_evaluators.automatability_llm_evaluator import AutomatabilityLlmEvaluator


class GeminiAutomatabilityEvaluationUnit(BaseAutomatabilityEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[EvaluationResult[Literal['yes', 'no']]]:
        llm_evaluator = AutomatabilityLlmEvaluator('gemini')
        result = llm_evaluator.evaluate(cve_id)
        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
