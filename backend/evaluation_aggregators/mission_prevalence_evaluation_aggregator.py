from typing import List, Literal

from evaluation_aggregators.base_evaluation_aggregator import BaseEvaluationAggregator
from evaluation_units.evaluation_unit import EvaluationUnit
from evaluation_units.mission_prevalence.base_mission_prevalence_evaluation_unit import \
    BaseMissionPrevalenceEvaluationUnit
from evaluation_units.mission_prevalence.gemini_mission_prevalence_evaluation_unit import \
    GeminiMissionPrevalenceEvaluationUnit
from evaluation_units.mission_prevalence.openai_mission_prevalence_evaluation_unit import \
    OpenaiMissionPrevalenceEvaluationUnit


class MissionPrevalenceEvaluationAggregator(BaseEvaluationAggregator):
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        super().__init__(llm)
        self._units: List[BaseMissionPrevalenceEvaluationUnit] = [
            GeminiMissionPrevalenceEvaluationUnit() if llm == 'gemini' else OpenaiMissionPrevalenceEvaluationUnit()
        ]

    def _get_units(self) -> List[EvaluationUnit]:
        return self._units
