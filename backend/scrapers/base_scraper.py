import logging

import requests

from utils import create_session, make_request


class BaseScraper:
    def __init__(self):
        self._session = create_session()

        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)

    def _make_request(self, url: str, max_retries: int = 3) -> requests.Response:
        return make_request(self._session, url, max_retries=max_retries, logger=self._logger)
