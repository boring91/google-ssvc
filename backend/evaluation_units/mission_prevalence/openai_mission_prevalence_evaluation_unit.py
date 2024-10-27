from typing import Optional, Literal

from evaluation_units.evaluation_unit import EvaluationResult
from evaluation_units.mission_prevalence.base_mission_prevalence_evaluation_unit import \
    BaseMissionPrevalenceEvaluationUnit
from llm.llm_evaluators.mission_prevalence_llm_evaluator import MissionPrevalenceLlmEvaluator


class OpenaiMissionPrevalenceEvaluationUnit(BaseMissionPrevalenceEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[
        EvaluationResult[Literal['minimal', 'support', 'essential']]]:
        llm_evaluator = MissionPrevalenceLlmEvaluator('openai')
        result = llm_evaluator.evaluate(cve_id)

        if result is None:
            return None

        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
