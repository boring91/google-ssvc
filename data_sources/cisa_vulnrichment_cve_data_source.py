import base64
import json
from typing import Optional

import requests

from data_sources.cve_data_source import CveDataSource


def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class CisaVulnrichmentCveDataSource(CveDataSource):
    def get_name(self) -> str:
        return 'cisa_vulnrichment'

    def _load_data(self, cve_id: str) -> Optional[dict]:
        [_, year, sub_id] = cve_id.split('-')

        base_url = 'https://api.github.com'
        owner = 'cisagov'
        repo = 'vulnrichment'

        # Load the available years
        repo_root_url = f'{base_url}/repos/{owner}/{repo}/contents'
        top_level = requests.get(repo_root_url).json()
        years = [x['name'] for x in top_level if x['type'] == 'dir' and _is_int(x['name'])]
        if year not in years:
            return None

        # Load the available groups in that year
        year_url = f'{repo_root_url}/{year}'
        year_level = requests.get(year_url).json()
        group = next((x for x in year_level if sub_id.startswith(x['name'].replace('x', ''))), None)

        # Load the cve data from the group
        cve_url = f'{year_url}/{group["name"]}/{cve_id}.json'
        cve_response = requests.get(cve_url)

        if 400 <= cve_response.status_code:
            return None

        cve_level = cve_response.json()
        cve_data = json.loads(base64.b64decode(cve_level['content']).decode('utf-8'))

        return cve_data
