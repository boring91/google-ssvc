from typing import Optional, Literal

from evaluation_units.evaluation_unit import EvaluationResult
from evaluation_units.mission_impact.base_mission_impact_evaluation_unit import BaseMissionImpactEvaluationUnit
from llm.llm_evaluators.mission_impact_llm_evaluator import MissionImpactLlmEvaluator


class OpenaiMissionImpactEvaluationUnit(BaseMissionImpactEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[
        EvaluationResult[Literal['degraded', 'mef_support_crippled', 'mef_failure', 'mission_failure']]]:
        llm_evaluator = MissionImpactLlmEvaluator('openai')
        result = llm_evaluator.evaluate(cve_id)
        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
