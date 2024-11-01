from typing import Optional, Literal

from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.public_wellbeing.base_public_wellbeing_evaluation_unit import BasePublicWellbeingEvaluationUnit
from ssvc.llm.llm_evaluators.public_wellbeing_llm_evaluator import PublicWellbeingLlmEvaluator


class GeminiPublicWellbeingEvaluationUnit(BasePublicWellbeingEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[
        EvaluationResult[Literal['minimal', 'material', 'irreversible']]]:
        llm_evaluator = PublicWellbeingLlmEvaluator('gemini')
        result = llm_evaluator.evaluate(cve_id)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
