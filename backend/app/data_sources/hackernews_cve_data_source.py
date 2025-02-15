from typing import Optional

import requests

from app.data_sources.cve_data_source import CveDataSource


class HackernewsCveDataSource(CveDataSource):
    @staticmethod
    def name() -> str:
        return 'hackernews'

    def _load_data(self, cve_id: str) -> Optional[dict]:
        url = f'https://hn.algolia.com/api/v1/search?query={cve_id}&tags=comment'

        response = requests.get(url)

        if response.status_code != 200:
            return None

        content = response.json()
        count = content['nbHits']
        if count == 0:
            return None

        data = {'excerpts': list(
            map(lambda x: {'title': x['story_title'], 'excerpt': x['comment_text'], 'source_url': x['story_url']},
                content['hits']))}

        return data
