from typing import Optional

from app.data_sources.nist_cve_data_source import NistCveDataSource
from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.value_density.base_value_density_evaluation_unit import BaseValueDensityEvaluationUnit
from ssvc.utils import extract_cvss_from_nist, standardize_cvss


class HeuristicValueDensityEvaluationUnit(BaseValueDensityEvaluationUnit):

    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        """
        Value density:
        IF Attack Vector (AV) is Network (AV:N)
            AND Privileges Required (PR) is None (PR:N)
            AND (Confidentiality Impact (VC) is High (VC:H)
                OR Integrity Impact (VI) is High (VI:H)
                OR Availability Impact (VA) is High (VA:H))
            THEN Value Density = Concentrated

        ELSE IF Attack Vector (AV) is Local (AV:L) or Adjacent (AV:A)
            OR Privileges Required (PR) is Low or High (PR:L or PR:H)
            OR User Interaction (UI) is Required (UI:R)
            THEN Value Density = Diffused

        ELSE IF Scope (S) is Changed (S:C)
            THEN Value Density = Concentrated

        ELSE
            Value Density = Diffused
        """

        data_source = NistCveDataSource()
        data = data_source.load(cve_id, reevaluate)
        cvss = extract_cvss_from_nist(data)

        if cvss is None:
            return None

        cvss = standardize_cvss(cvss)

        if 'AV:N' in cvss and 'PR:N' in cvss and ('VC:H' in cvss or 'VI:H' in cvss or 'VA:H' in cvss):
            return EvaluationResult(
                'concentrated',
                1,
                'Rule-based heuristic evaluation using the cvss vector string.',
                [])

        if 'AV:L' in cvss or 'AV:A' in cvss or 'PR:L' in cvss or 'PR:H' in cvss or 'UI:R' in cvss:
            return EvaluationResult(
                'diffused',
                1,
                'Rule-based heuristic evaluation using the cvss vector string.',
                [])

        if 'S:C' in cvss:
            return EvaluationResult(
                'concentrated',
                1,
                'Rule-based heuristic evaluation using the cvss vector string.',
                [])

        return EvaluationResult('diffused', 1, 'Rule-based heuristic evaluation using the cvss vector string.', [])
