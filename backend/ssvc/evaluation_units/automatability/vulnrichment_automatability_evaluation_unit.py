from typing import Optional, Literal

from app.data_sources.cisa_vulnrichment_cve_data_source import CisaVulnrichmentCveDataSource
from ssvc.evaluation_units.automatability.base_automatability_evaluation_unit import BaseAutomatabilityEvaluationUnit
from ssvc.evaluation_units.evaluation_unit import EvaluationResult


class VulnrichmentAutomatabilityEvaluationUnit(BaseAutomatabilityEvaluationUnit):

    def _process_evaluation(self, cve_id: str) -> Optional[EvaluationResult[Literal['yes', 'no']]]:
        data_source = CisaVulnrichmentCveDataSource()

        result = data_source.load(cve_id)
        if result is None:
            return None

        return EvaluationResult(result['automatable'], 1, 'Found in the CISA Vulnrichment data set.')
