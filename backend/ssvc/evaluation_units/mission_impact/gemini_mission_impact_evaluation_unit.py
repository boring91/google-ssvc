from typing import Optional, Literal

from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.mission_impact.base_mission_impact_evaluation_unit import BaseMissionImpactEvaluationUnit
from ssvc.llm.llm_evaluators.mission_impact_llm_evaluator import MissionImpactLlmEvaluator


class GeminiMissionImpactEvaluationUnit(BaseMissionImpactEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[
        EvaluationResult[Literal['degraded', 'mef_support_crippled', 'mef_failure', 'mission_failure']]]:
        llm_evaluator = MissionImpactLlmEvaluator('gemini')
        result = llm_evaluator.evaluate(cve_id)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
