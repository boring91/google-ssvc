import base64
import json
import os
from typing import Optional, List

import requests

from app.data_sources.cve_data_source import CveDataSource


def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class CisaVulnrichmentCveDataSource(CveDataSource):
    @staticmethod
    def name() -> str:
        return 'cisa'

    def _load_data(self, cve_id: str) -> Optional[dict]:
        tokens = cve_id.split('-')
        if len(tokens) != 3:
            return None

        [_, year, sub_id] = cve_id.split('-')

        base_url = 'https://api.github.com'
        owner = 'cisagov'
        repo = 'vulnrichment'
        headers = {
            'Authorization': f'Bearer {os.getenv("GITHUB_PAT")}'
        } if os.getenv('GITHUB_PAT') is not None else {}

        # Load the available years
        repo_root_url = f'{base_url}/repos/{owner}/{repo}/contents'
        top_level = requests.get(repo_root_url, headers=headers).json()
        years = [x['name'] for x in top_level if x['type'] == 'dir' and _is_int(x['name'])]
        if year not in years:
            return None

        # Load the available groups in that year
        year_url = f'{repo_root_url}/{year}'
        year_level = requests.get(year_url, headers=headers).json()
        group = next((x for x in year_level if sub_id.startswith(x['name'].replace('x', ''))), None)
        if group is None:
            return None

        # Load the cve data from the group
        cve_url = f'{year_url}/{group["name"]}/{cve_id}.json'
        cve_response = requests.get(cve_url, headers=headers)

        if 400 <= cve_response.status_code:
            return None

        cve_level = cve_response.json()
        cve_data = json.loads(base64.b64decode(cve_level['content']).decode('utf-8'))

        # Search for the data of interest
        if 'containers' not in cve_data:
            return None

        containers = cve_data['containers']
        if 'adp' not in containers:
            return None

        adp: List = containers['adp']
        if len(adp) == 0:
            return None

        for adp_item in adp:
            if 'metrics' not in adp_item:
                continue

            metrics: List = adp_item['metrics']
            if len(metrics) == 0:
                continue

            for metrics_item in metrics:
                if 'other' not in metrics_item:
                    continue

                other = metrics_item['other']
                if 'content' not in other or 'type' not in other or other['type'] != 'ssvc':
                    continue

                content = other['content']
                if 'options' not in content:
                    return None

                options = content['options']
                result = {list(item.keys())[0].lower().replace(' ', '_'): list(item.values())[0] for item in options}
                result['link'] = cve_url
                return result

        return None
