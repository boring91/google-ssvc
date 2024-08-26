from typing import List

from cve_data_source import CveDataSource
from vulners_cve_data_source import VulnersCveDataSource


class CveDataSourceAggregator:
    def __init__(self):
        self._data_sources: List[CveDataSource] = [
            VulnersCveDataSource()
        ]

    def load(self, cve_id: str) -> dict:
        return self._data_sources[0].load(cve_id)
