from abc import abstractmethod
from typing import Literal, Optional

from ssvc.evaluation_units.evaluation_unit import EvaluationUnit, EvaluationResult


class BaseTechnicalImpactEvaluationUnit(EvaluationUnit):
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
        return 'technical_impact'

    @abstractmethod
    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        pass
