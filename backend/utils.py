import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def create_session() -> requests.Session:
    session = requests.Session()

    adapter = HTTPAdapter(
        pool_connections=50,
        pool_maxsize=100,
        max_retries=Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]))
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session


def make_request(
        session: requests.Session,
        url: str,
        headers: dict = None,
        max_retries: int = 3,
        logger: logging.Logger = None,
        timeout=10) -> requests.Response:
    for attempt in range(max_retries):
        try:
            response = session.get(url, timeout=timeout, headers={} if headers is None else headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                if logger is not None:
                    logger.error(f'Failed to fetch {url} after {max_retries} attempts: {e}')
                raise
            time.sleep(1 * (attempt + 1))
