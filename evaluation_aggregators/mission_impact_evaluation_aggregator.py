from typing import List, Literal

from evaluation_aggregators.base_evaluation_aggregator import BaseEvaluationAggregator
from evaluation_units.evaluation_unit import EvaluationUnit
from evaluation_units.mission_impact.base_mission_impact_evaluation_unit import BaseMissionImpactEvaluationUnit
from evaluation_units.mission_impact.gemini_mission_impact_evaluation_unit import GeminiMissionImpactEvaluationUnit
from evaluation_units.mission_impact.openai_mission_impact_evaluation_unit import OpenaiMissionImpactEvaluationUnit


class MissionImpactEvaluationAggregator(BaseEvaluationAggregator):
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        super().__init__(llm)
        self._units: List[BaseMissionImpactEvaluationUnit] = [
            GeminiMissionImpactEvaluationUnit() if llm == 'gemini' else OpenaiMissionImpactEvaluationUnit()
        ]

    def _get_units(self) -> List[EvaluationUnit]:
        return self._units
