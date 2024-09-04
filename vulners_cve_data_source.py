import os
import json
from typing import Optional

import vulners

from cve_data_source import CveDataSource


class VulnersCveDataSource(CveDataSource):
    def __init__(self):
        super().__init__()
        self._vulners_api = vulners.VulnersApi(api_key=os.getenv('VULNERS_API_KEY'))

    def _load_data(self, cve_id: str) -> Optional[dict]:
        try:
            return self._vulners_api.get_bulletin(cve_id, fields=["*"])
        except:
            return None

    def get_name(self) -> str:
        return 'vulners'
