from typing import Optional, Literal

from evaluation_units.evaluation_unit import EvaluationResult
from evaluation_units.technical_impact.base_technical_impact_evaluation_unit import BaseTechnicalImpactEvaluationUnit
from llm.llm_evaluators.technical_impact_llm_evaluator import TechnicalImpactLlmEvaluator


class OpenaiTechnicalImpactEvaluationUnit(BaseTechnicalImpactEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[EvaluationResult[Literal['partial', 'total']]]:
        llm_evaluator = TechnicalImpactLlmEvaluator('openai')
        result = llm_evaluator.evaluate(cve_id)
        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
