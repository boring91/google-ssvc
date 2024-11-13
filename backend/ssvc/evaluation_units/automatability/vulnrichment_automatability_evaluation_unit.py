from typing import Optional

from app.data_sources.cisa_vulnrichment_cve_data_source import CisaVulnrichmentCveDataSource
from ssvc.evaluation_units.automatability.base_automatability_evaluation_unit import BaseAutomatabilityEvaluationUnit
from ssvc.evaluation_units.evaluation_unit import EvaluationResult


class VulnrichmentAutomatabilityEvaluationUnit(BaseAutomatabilityEvaluationUnit):

    def _process_evaluation(self, cve_id: str, reevaluate: bool) -> Optional[EvaluationResult]:
        data_source = CisaVulnrichmentCveDataSource()

        result = data_source.load(cve_id, reevaluate)
        if result is None:
            return None

        return EvaluationResult(result['automatable'], 1, 'Found in the CISA Vulnrichment data set.', [result['link']])
