from typing import List

from data_sources.cisa_kev_cve_data_source import CisaKevCveDataSource
from data_sources.cisa_vulnrichment_cve_data_source import CisaVulnrichmentCveDataSource
from data_sources.cve_data_source import CveDataSource
from data_sources.nist_cve_data_source import NistCveDataSource
from data_sources.vulners_cve_data_source import VulnersCveDataSource


class CveDataSourceAggregator:
    def __init__(self):
        self._data_sources: List[CveDataSource] = [
            VulnersCveDataSource(),
            NistCveDataSource(),
            CisaKevCveDataSource(),
            CisaVulnrichmentCveDataSource()
        ]

    def load(self, cve_id: str) -> dict:
        aggregated_data = dict()

        for data_source in self._data_sources:
            data = data_source.load(cve_id)

            if data is None:
                continue

            aggregated_data[f'{data_source.name()}_data_source'] = data

        return aggregated_data
