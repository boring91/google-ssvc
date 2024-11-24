import json

import requests

from database.db import Db
import os
import time
import concurrent.futures
from utils import create_session, make_request


def start_nist_fetcher():
    # Read the cves
    with open('./cves.txt') as f:
        vuln = f.readlines()

    vuln = list(set([x.split(' ')[0] for x in vuln]))
    vuln = [x for x in vuln if x.startswith('CVE')]
    vuln.sort()

    # Initialize
    session = create_session()
    cool_off_period = 60
    batch_size = 50
    batches = [vuln[i:i + batch_size] for i in range(0, len(vuln), batch_size)]

    def fetch(vuln_id: str):
        base_url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
        url = f'{base_url}?cveId={vuln_id}'
        response = make_request(session, url, headers={'apiKey': os.getenv('NIST_API_KEY')}, timeout=60)
        vuln_data = response.json()['vulnerabilities'][0]['cve']

        with Db() as db:
            db.execute(
                """
                INSERT INTO cve_cache(cve_id, source, data) VALUES (%s, %s, %s) 
                ON CONFLICT (cve_id, source) DO NOTHING;
                """,

                (vuln_id, 'nist', json.dumps(vuln_data)))

    def start():
        for idx, batch in enumerate(batches):
            print(f'batch number {idx + 1}/{len(batches)}')
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(fetch, vuln_id) for vuln_id in batch]
                concurrent.futures.wait(futures)

            time.sleep(cool_off_period)

    start()


def start_osv_fetcher():
    # Read the cves
    with open('./cves.txt') as f:
        vuln = f.readlines()

    vuln = list(set([x.split(' ')[0] for x in vuln]))
    vuln.sort()

    # Initialize
    session = create_session()

    def fetch(vuln_id: str):
        base_url = 'https://api.osv.dev/v1/vulns'
        url = f'{base_url}/{vuln_id}'
        response = make_request(session, url)

        if not (200 <= response.status_code < 300):
            return

        vuln_data = response.json()

        with Db() as db:
            db.execute(
                """
                INSERT INTO cve_cache(cve_id, source, data) VALUES (%s, %s, %s) 
                ON CONFLICT (cve_id, source) DO NOTHING;
                """,

                (vuln_id, 'osv', json.dumps(vuln_data)))

    def start():
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(fetch, vuln_id) for vuln_id in vuln]
            concurrent.futures.wait(futures)

    start()


def start_kev_fetcher():
    response = requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
    items = response.json()['vulnerabilities']

    def store(item: dict):
        with Db() as db:
            db.execute(
                """
                INSERT INTO cve_cache(cve_id, source, data) VALUES (%s, %s, %s) 
                ON CONFLICT (cve_id, source) DO NOTHING;
                """,

                (item['cveID'], 'kev', json.dumps(item)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(store, item) for item in items]
        concurrent.futures.wait(futures)
