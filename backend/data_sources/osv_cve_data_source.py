from typing import Optional

import requests

from data_sources.cve_data_source import CveDataSource


class OsvCveDataSource(CveDataSource):
    @staticmethod
    def name() -> str:
        return 'osv'

    def _load_data(self, cve_id: str) -> Optional[dict]:
        url = f'https://api.osv.dev/v1/vulns/{cve_id}'
        response = requests.get(url)

        if not (200 <= response.status_code < 300):
            return None

        return response.json();
