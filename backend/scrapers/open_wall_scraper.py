import concurrent.futures
from datetime import datetime
from typing import Literal

from elasticsearch import Elasticsearch
from lxml import html

from base_scraper import BaseScraper


class OpenWallScraper(BaseScraper):
    def __init__(
            self,
            source: Literal['oss-security', 'bugtraq', 'full-disclosure'],
            elasticsearch_url: str = 'http://localhost:9200',
            index_name: str = 'security-blogs',
            create_index: bool = False):
        super().__init__()
        self._source = source
        self._es = Elasticsearch(elasticsearch_url)
        self._index_name = index_name
        self._base_url = 'https://www.openwall.com/lists/oss-security' if source == 'oss-security' \
            else 'https://lists.openwall.net/bugtraq' if source == 'bugtraq' \
            else 'https://lists.openwall.net/full-disclosure'

        # Initialize index
        if create_index:
            self._setup_index()

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
                'source': self._source,
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
