from typing import Optional

from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.mission_impact.base_mission_impact_evaluation_unit import BaseMissionImpactEvaluationUnit
from ssvc.llm.llm_evaluators.mission_impact_llm_evaluator import MissionImpactLlmEvaluator


class OpenaiMissionImpactEvaluationUnit(BaseMissionImpactEvaluationUnit):
    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        llm_evaluator = MissionImpactLlmEvaluator('openai')
        result = llm_evaluator.evaluate(cve_id, reevaluate)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'], result['links'])
