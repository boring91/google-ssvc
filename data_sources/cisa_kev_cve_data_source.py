import json
import os.path
from typing import Optional, List

import requests

from data_sources.cve_data_source import CveDataSource


class CisaKevCveDataSource(CveDataSource):
    def __init__(self):
        super().__init__()

        # Download the db if it does not exist
        self.db_path = os.path.join('.', 'data', 'cisa_kev_db.json')
        if not os.path.exists(self.db_path):
            url = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'
            response = requests.get(url)
            db = response.json()

            with open(self.db_path, 'w') as f:
                json.dump(db, f)

    def get_name(self) -> str:
        return 'cisa_kev'

    def _load_data(self, cve_id: str) -> Optional[dict]:
        db = self._get_db()
        vulnerabilities: List[dict] = db['vulnerabilities']
        cve_data = next((x for x in vulnerabilities if x['cveID'] == cve_id), None)
        return cve_data

    def _get_db(self) -> dict:
        with open(self.db_path, 'r') as f:
            db = json.load(f)
            return db
