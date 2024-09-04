from typing import List

from cve_data_source import CveDataSource
from nist_cve_data_source import NistCveDataSource
from vulners_cve_data_source import VulnersCveDataSource


class CveDataSourceAggregator:
    def __init__(self):
        self._data_sources: List[CveDataSource] = [
            VulnersCveDataSource(),
            NistCveDataSource()
        ]

    def load(self, cve_id: str) -> dict:
        aggregated_data = dict()

        for data_source in self._data_sources:
            data = data_source.load(cve_id)

            if data is None:
                continue

            aggregated_data[f'{data_source.get_name()}_data_source'] = data

        return aggregated_data
