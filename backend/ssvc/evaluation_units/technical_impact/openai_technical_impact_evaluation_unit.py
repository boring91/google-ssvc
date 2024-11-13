from typing import Optional

from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.technical_impact.base_technical_impact_evaluation_unit import \
    BaseTechnicalImpactEvaluationUnit
from ssvc.llm.llm_evaluators.technical_impact_llm_evaluator import TechnicalImpactLlmEvaluator


class OpenaiTechnicalImpactEvaluationUnit(BaseTechnicalImpactEvaluationUnit):
    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        llm_evaluator = TechnicalImpactLlmEvaluator('openai')
        result = llm_evaluator.evaluate(cve_id, reevaluate)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'], result['links'])
