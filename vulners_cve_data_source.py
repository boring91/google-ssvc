import os
import json
from typing import Optional

import vulners

from cve_data_source import CveDataSource


class VulnersCveDataSource(CveDataSource):
    def __init__(self, cache_path='vulners'):
        self._vulners_api = vulners.VulnersApi(api_key=os.getenv('VULNERS_API_KEY'))
        self._cache_path = cache_path
        os.makedirs(os.path.join('.', 'data', self._cache_path), exist_ok=True)

    def load(self, cve_id: str) -> Optional[dict]:
        cve_id = cve_id.upper()

        cve_file_path = os.path.join('.', 'data', self._cache_path, f'{cve_id}.json')

        # check if we have a cached data of the cve then
        # return it.
        if os.path.exists(cve_file_path):
            with open(cve_file_path, 'r') as f:
                return json.load(f)

        cve_data = self._vulners_api.get_bulletin(cve_id, fields=["*"])

        # cache the data
        with open(cve_file_path, 'w') as f:
            json.dump(cve_data, f)

        return cve_data
