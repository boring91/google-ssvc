from typing import Optional, Literal

from evaluation_units.evaluation_unit import EvaluationResult
from evaluation_units.mission_prevalence.base_mission_prevalence_evaluation_unit import \
    BaseMissionPrevalenceEvaluationUnit
from llm.llm_evaluators.mission_prevalence_llm_evaluator import MissionPrevalenceLlmEvaluator


class GeminiMissionPrevalenceEvaluationUnit(BaseMissionPrevalenceEvaluationUnit):
    def _process_evaluation(self, cve_id: str) -> Optional[
        EvaluationResult[Literal['minimal', 'support', 'essential']]]:
        llm_evaluator = MissionPrevalenceLlmEvaluator('gemini')
        result = llm_evaluator.evaluate(cve_id)
        return EvaluationResult(result['assessment'], result['confidence'], result['justification'])
