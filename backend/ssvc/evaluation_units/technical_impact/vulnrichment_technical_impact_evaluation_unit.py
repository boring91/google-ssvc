from typing import Optional, Literal

from app.data_sources.cisa_vulnrichment_cve_data_source import CisaVulnrichmentCveDataSource
from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.evaluation_units.technical_impact.base_technical_impact_evaluation_unit import BaseTechnicalImpactEvaluationUnit


class VulnrichmentTechnicalImpactEvaluationUnit(BaseTechnicalImpactEvaluationUnit):

    def _process_evaluation(self, cve_id: str) -> Optional[EvaluationResult]:
        data_source = CisaVulnrichmentCveDataSource()

        result = data_source.load(cve_id)
        if result is None:
            return None

        return EvaluationResult(result['technical_impact'], 1, 'Found in the CISA Vulnrichment data set.')
