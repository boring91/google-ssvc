from abc import abstractmethod
from typing import Optional


class CveDataSource:
    @abstractmethod
    def load(self, cve_id: str) -> Optional[dict]:
        pass
