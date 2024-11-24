import concurrent.futures
import json

import requests
from lxml import html

from base_scraper import BaseScraper
from database.db import Db


class CisaVulnrichmentScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self._base_url = 'https://github.com/cisagov/vulnrichment/tree/develop'
        self._content_base_url = 'https://raw.githubusercontent.com/cisagov/vulnrichment/refs/heads/develop'

    def scrape(self):
        try:
            response = self._make_request(self._base_url)

            tree = html.fromstring(response.content)
            repo = json.loads(tree.xpath('string(//react-partial[@partial-name="repos-overview"]/script)'))
            items = repo['props']['initialPayload']['tree']['items']
            years = [x['name'].split('/')[0] for x in items if x['name'].isdigit() or x['name'].split('/')[0].isdigit()]

            for year in years:
                self._logger.info(f'Starting to scrape year {year}')
                self._scrape_year(year)
        except Exception as e:
            self._logger.error(f'Error in main scraping process: {e}')

    def _scrape_year(self, year: str):
        url = f'{self._base_url}/{year}'

        try:
            response = requests.get(url)
            tree = html.fromstring(response.content)
            repo = json.loads(tree.xpath('string(//react-app[@app-name="react-code-view"]/script)'))
            items = repo['payload']['tree']['items']
            groups = [x['name'] for x in items]

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [
                    executor.submit(self._scrape_group, year, group)
                    for group in groups
                ]
                concurrent.futures.wait(futures)
        except Exception as e:
            self._logger.error(f'Error processing year {url}: {e}')

    def _scrape_group(self, year: str, group: str):
        url = f'{self._base_url}/{year}/{group}'
        try:
            response = requests.get(url)
            tree = html.fromstring(response.content)
            repo = json.loads(tree.xpath('string(//react-app[@app-name="react-code-view"]/script)'))
            items = repo['payload']['tree']['items']
            files = [x['name'] for x in items]

            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                futures = [
                    executor.submit(self._scrape_file, year, group, file)
                    for file in files
                ]
                concurrent.futures.wait(futures)

        except Exception as e:
            self._logger.error(f'Error processing group {group}: {e}')

    def _scrape_file(self, year: str, group: str, file: str):
        url = f'{self._content_base_url}/{year}/{group}/{file}'
        try:
            response = requests.get(url)
            cve_data = response.json()
            cve_id = file.split('.')[0].upper()

            with Db() as db:
                db.execute(
                    """
                    INSERT INTO cve_cache(cve_id, source, data) VALUES (%s, %s, %s) 
                    ON CONFLICT (cve_id, source) DO NOTHING;
                    """,
                    (cve_id, 'vulnrichment', json.dumps(cve_data)))

        except Exception as e:
            self._logger.error(f'Error processing file {file}: {e}')
