from abc import abstractmethod
from typing import Literal, Optional

from evaluation_units.evaluation_unit import EvaluationUnit, EvaluationResult


class BaseMissionImpactEvaluationUnit(EvaluationUnit):
    @staticmethod
    def type() -> Literal[
        'state_of_exploitation',
        'automatability',
        'technical_impact',
        'value_density',
        'exposure',
        'mission_impact',
        'mission_prevalence',
        'public_wellbeing']:
        return 'mission_impact'

    @abstractmethod
    def _process_evaluation(self, cve_id: str) -> Optional[
        EvaluationResult[Literal['degraded', 'mef_support_crippled', 'mef_failure', 'mission_failure']]]:
        pass
