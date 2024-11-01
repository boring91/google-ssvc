from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class EvaluationResult:
    assessment: str
    confidence: float
    justification: str


class EvaluationUnit:
    """
    The purpose of an evaluation unit is; given a cve, to evaluate said
    cve on one of the decision points.
    """

    @staticmethod
    @abstractmethod
    def type() -> Literal[
        'state_of_exploitation',
        'automatability',
        'technical_impact',
        'value_density',
        'exposure',
        'mission_impact',
        'mission_prevalence',
        'public_wellbeing']:
        pass

    def evaluate(self, cve_id: str) -> Optional[EvaluationResult]:
        return self._process_evaluation(cve_id.upper())

    @abstractmethod
    def _process_evaluation(self, cve_id: str) -> Optional[EvaluationResult]:
        pass
