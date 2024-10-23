from typing import Optional, Literal

from evaluation_units.evaluation_unit import EvaluationResult
from evaluation_units.value_density.base_value_density_evaluation_unit import BaseValueDensityEvaluationUnit
from llm.llm_evaluators.value_density_llm_evaluator import ValueDensityLlmEvaluator


class OpenaiValueDensityEvaluationUnit(BaseValueDensityEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[EvaluationResult[Literal['centralized', 'diffused']]]:
        llm_evaluator = ValueDensityLlmEvaluator('openai')
        result = llm_evaluator.evaluate(cve_id)
        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
