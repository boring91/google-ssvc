import json
import logging
from abc import abstractmethod
from typing import Optional

from database.db import Db


class CveDataSource:
    def __init__(self):
        self._source_name = self.__class__.name()

        self._logger = logging.getLogger(self.__class__.__name__)

    def load(self, cve_id: str, reload: bool = False) -> Optional[dict]:
        cve_id = cve_id.upper()
        if not reload:
            with Db() as db:
                cached_data = db.first('SELECT * FROM cve_cache WHERE cve_id = %s AND source = %s',
                                       (cve_id, self._source_name))

            if cached_data is not None:
                return json.loads(cached_data['data'])

            self._logger.info(f'No cached data was found for cve {cve_id}, loading from data source.')

        else:
            with Db() as db:
                db.execute('DELETE FROM cve_cache WHERE cve_id = %s AND source = %s',
                           (cve_id, self._source_name))

        cve_data = self._load_data(cve_id)

        if cve_data is None:
            return None

        # cache the data
        with Db() as db:
            db.execute(
                """
                INSERT INTO cve_cache(cve_id, source, data) VALUES (%s, %s, %s) 
                ON CONFLICT (cve_id, source) DO NOTHING;
                """,
                (cve_id, self._source_name, json.dumps(cve_data)))

        return cve_data

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    def _load_data(self, cve_id: str) -> Optional[dict]:
        pass
