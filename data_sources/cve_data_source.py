import json
import os
from abc import abstractmethod
from typing import Optional


class CveDataSource:
    def __init__(self):
        source_name = self.get_name()
        self._cache_path = os.path.join('..', 'data', 'cve_data_source_cache', source_name)
        os.makedirs(self._cache_path, exist_ok=True)

    def load(self, cve_id: str) -> Optional[dict]:
        cve_id = cve_id.upper()

        cve_file_path = os.path.join(self._cache_path, f'{cve_id}.json')

        # check if we have a cached data of the cve then
        # return it.
        if os.path.exists(cve_file_path):
            with open(cve_file_path, 'r') as f:
                return json.load(f)

        cve_data = self._load_data(cve_id)

        if cve_data is None:
            return None

        # cache the data
        with open(cve_file_path, 'w') as f:
            json.dump(cve_data, f)

        return cve_data

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def _load_data(self, cve_id: str) -> Optional[dict]:
        pass
