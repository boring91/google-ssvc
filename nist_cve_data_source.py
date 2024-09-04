from typing import Optional

import requests

from cve_data_source import CveDataSource


class NistCveDataSource(CveDataSource):

    def _load_data(self, cve_id: str) -> Optional[dict]:
        base_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
        url = f'{base_url}?cveId={cve_id}'

        response = requests.get(url)

        if response.status_code != 200:
            return None

        try:
            return dict(response.json()['vulnerabilities'][0]['cve'])
        except:
            return None

    def get_name(self) -> str:
        return 'nist'
