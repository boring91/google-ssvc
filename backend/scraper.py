import concurrent.futures
from elasticsearch import Elasticsearch
import requests
from datetime import datetime
from lxml import html
import time
import logging

from requests.adapters import HTTPAdapter
from urllib3 import Retry


class SecurityMailingScraper:
    def __init__(
            self,
            elasticsearch_url: str = 'http://localhost:9200',
            index_name: str = 'security-blogs'):
        self._es = Elasticsearch(elasticsearch_url)
        self._index_name = index_name
        # self._base_url = 'https://www.openwall.com/lists/oss-security'
        # self._base_url = 'https://lists.openwall.net/bugtraq'
        self._base_url = 'https://lists.openwall.net/full-disclosure'

        self._session = requests.Session()
        adapter = HTTPAdapter(
            pool_connections=50,  # Number of connection objects to keep in pool
            pool_maxsize=100,  # Maximum number of connections to keep in pool
            max_retries=Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504]
            )
        )
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)

        # Initialize index
        # self._setup_index()

    def _setup_index(self):
        """Setup Elasticsearch index with proper mappings"""
        if self._es.indices.exists(index=self._index_name):
            self._es.indices.delete(index=self._index_name)

        mappings = {
            'properties': {
                'year': {'type': 'integer'},
                'month': {'type': 'integer'},
                'day': {'type': 'integer'},
                'timestamp': {'type': 'date'},
                'source': {'type': 'keyword'},
                'source_type': {'type': 'keyword'},
                'url': {'type': 'keyword'},
                'content': {'type': 'text', 'analyzer': 'standard'}
            }
        }

        self._es.options(ignore_status=[400]).indices.create(
            index=self._index_name,
            mappings=mappings
        )

    def _make_request(self, url: str, max_retries: int = 3) -> requests.Response:
        """Make HTTP request with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self._session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    self._logger.error(f"Failed to fetch {url} after {max_retries} attempts: {e}")
                    raise
                time.sleep(1 * (attempt + 1))  # Exponential backoff

    def _scrape_item(self, year: str, month: str, day: str, item: str):
        """Scrape individual mail item"""
        url = f'{self._base_url}/{year}{month}{day}{item}'
        try:
            response = self._make_request(url)
            tree = html.fromstring(response.content)
            content = tree.xpath('string(//pre)')

            document = {
                'year': int(year[:-1]),
                'month': int(month[:-1]),
                'day': int(day[:-1]),
                'timestamp': datetime.utcnow(),
                # 'source': 'oss-security',
                # 'source': 'bugtraq',
                'source': 'full-disclosure',
                'source_type': 'mailing_list',
                'url': url,
                'content': content
            }

            self._es.index(index=self._index_name, document=document)
            self._logger.debug(f"Indexed document from {url}")

        except Exception as e:
            self._logger.error(f"Error processing {url}: {e}")

    def _scrape_day(self, year: str, month: str, day: str):
        """Scrape all items for a given day"""
        url = f'{self._base_url}/{year}{month}{day}'
        try:
            response = self._make_request(url)
            tree = html.fromstring(response.content)
            items = tree.xpath('//h2/following-sibling::ul[1]/li/a/@href')

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [
                    executor.submit(self._scrape_item, year, month, day, item)
                    for item in items
                ]
                concurrent.futures.wait(futures)

        except Exception as e:
            self._logger.error(f"Error processing day {url}: {e}")

    def _scrape_month(self, year: str, month: str):
        """Scrape all days in a month"""
        url = f'{self._base_url}/{year}{month}'
        try:
            response = self._make_request(url)
            tree = html.fromstring(response.content)
            days = tree.xpath('//table[@class="cal_mon"]/tr/td/a/@href')

            # Process days in parallel with a maximum of 3 concurrent days
            with concurrent.futures.ThreadPoolExecutor(max_workers=31) as executor:
                futures = [
                    executor.submit(self._scrape_day, year, month, day)
                    for day in days
                ]
                concurrent.futures.wait(futures)

        except Exception as e:
            self._logger.error(f"Error processing month {url}: {e}")

    def _scrape_year(self, year: str):
        """Scrape all months in a year"""
        url = f'{self._base_url}/{year}'
        try:
            response = self._make_request(url)
            tree = html.fromstring(response.content)
            months = tree.xpath('//table[@class="cal_brief"]/tr[2]/td/a/@href')

            # Process months sequentially to maintain order and avoid overwhelming the server
            for month in months:
                self._logger.info(f"Scraping {year}{month}")
                self._scrape_month(year, month)

        except Exception as e:
            self._logger.error(f"Error processing year {url}: {e}")

    def scrape(self, max_years: int = None):
        """Main scraping entry point"""
        try:
            response = self._make_request(self._base_url)
            tree = html.fromstring(response.content)
            years = tree.xpath('//table[@class="cal_brief"]/tr/td[1]/a/@href')

            if max_years:
                years = years[:max_years]

            for year in years:
                self._logger.info(f"Starting to scrape year {year[:-1]}")
                self._scrape_year(year)

        except Exception as e:
            self._logger.error(f"Error in main scraping process: {e}")


if __name__ == "__main__":
    scraper = SecurityMailingScraper()
    scraper.scrape(max_years=1)  # Scrape only the most recent year
