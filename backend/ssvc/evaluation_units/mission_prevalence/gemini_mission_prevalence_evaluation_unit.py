from typing import Optional

from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.mission_prevalence.base_mission_prevalence_evaluation_unit import \
    BaseMissionPrevalenceEvaluationUnit
from ssvc.llm.llm_evaluators.mission_prevalence_llm_evaluator import MissionPrevalenceLlmEvaluator


class GeminiMissionPrevalenceEvaluationUnit(BaseMissionPrevalenceEvaluationUnit):
    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        llm_evaluator = MissionPrevalenceLlmEvaluator('gemini')
        result = llm_evaluator.evaluate(cve_id, reevaluate)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'], result['links'])
