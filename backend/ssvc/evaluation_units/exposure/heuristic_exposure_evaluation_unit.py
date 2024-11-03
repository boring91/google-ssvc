from typing import Optional

from app.data_sources.nist_cve_data_source import NistCveDataSource
from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.exposure.base_exposure_evaluation_unit import BaseExposureEvaluationUnit
from ssvc.utils import extract_cvss_from_nist, standardize_cvss


class HeuristicExposureEvaluationUnit(BaseExposureEvaluationUnit):

    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        """
        Exposure:
        if AV == "N" and PR == "N" and UI == "N":
            return "open"
        else if AV in ["N", "A"] and (PR in ["L", "H"] or UI == "R"):
            return "controlled"
        else if AV in ["L", "P"]
            return "small"
        """

        data_source = NistCveDataSource()
        data = data_source.load(cve_id, reevaluate)
        cvss = extract_cvss_from_nist(data)

        if cvss is None:
            return None

        cvss = standardize_cvss(cvss)

        if 'AV:N' in cvss and 'PR:N' and 'UI:N':
            return EvaluationResult('open', 1, 'Rule-based heuristic evaluation.')

        if ('AV:N' in cvss or 'AV:A' in cvss) and ('PR:L' in cvss or 'PR:H' in cvss or 'UI:R' in cvss):
            return EvaluationResult('controlled', 1, 'Rule-based heuristic evaluation.')

        if 'AV:L' in cvss or 'AV:P' in cvss:
            return EvaluationResult('small', 1, 'Rule-based heuristic evaluation.')

        return None
