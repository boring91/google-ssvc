from typing import Optional, List

import requests

from app.data_sources.cve_data_source import CveDataSource


class CisaKevCveDataSource(CveDataSource):
    def __init__(self):
        super().__init__()

    @staticmethod
    def name() -> str:
        return 'cisa_kev'

    def _load_data(self, cve_id: str) -> Optional[dict]:
        url = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'
        response = requests.get(url)
        db = response.json()

        vulnerabilities: List[dict] = db['vulnerabilities']
        cve_data = next((x for x in vulnerabilities if x['cveID'] == cve_id), None)
        return cve_data
