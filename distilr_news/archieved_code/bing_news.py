import json
import logging
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import time
import requests
import pprint


from .bing_entity import BingEntity
from .timeline_content import Content


LOG = logging.getLogger(__name__)


class BingNewsApi:

    def __init__(self, auth_key):
        self.auth_key = auth_key


    def search_entities(self, query):
        response = requests.get(
            'https://api.cognitive.microsoft.com/bing/v7.0/entities',
            headers={
                'Ocp-Apim-Subscription-Key': self.auth_key
            },
            params={
                # See https://docs.microsoft.com/en-us/previous-versions/bing/search/ff795620(v=msdn.10)?redirectedfrom=MSDN 
                'q': query,
                'mkt': 'en-us',
            }
        )
        if not response.ok:
            response.raise_for_error()

        response_json = response.json()
        LOG.info(response_json)
        if 'entities' not in response_json:
            return None
        if 'value' not in response_json['entities']:
            return None
        
        bing_entity = None
        for entity in response.json()['entities']['value']:
            # NOTE: Done because I'm not sure if these come in order 
            if entity['entityPresentationInfo']['entityScenario'] != 'DominantEntity':
                continue
            bing_entity = BingEntity(
                entity['bingId'],
                entity['name'], 
                entity['description'],
                entity.get('entityPresentationInfo', None),
                entity.get('image', None)
            )
            return bing_entity


    def _search_news(self, query, time_start, time_end):
        response = requests.get(
            'https://api.cognitive.microsoft.com/bing/v7.0/news/search',
            headers={
                'Ocp-Apim-Subscription-Key': self.auth_key
            },
            params={
                # See https://docs.microsoft.com/en-us/previous-versions/bing/search/ff795620(v=msdn.10)?redirectedfrom=MSDN 
                'q': query,
                'mkt': 'en-us',
                'count': 100,
            }
        )
        if not response.ok:
            response.raise_for_error()
        return response.json()['value']


    def get_timeline_content(self, bing_entity, time_start, time_end):

        contents = []
        for article in self._search_news(bing_entity.name, None, None):
            LOG.info(article.keys())
            LOG.info(article)
            LOG.info('-'*25)
            if 'about' in article:
                for entity in article['about']:
                    possible_id = entity['readLink'].split('/')[-1]
                    LOG.info('{} ? {}'.format(possible_id, bing_entity.id))
                    if possible_id == bing_entity.id:
                        try:
                            published_at = datetime.fromisoformat(article['datePublished'])
                        except Exception as e:
                            published_at = datetime.fromisoformat(article['datePublished'][:26])
                        
                        content = Content(
                            article['name'],
                            article['url'],
                            article['description'],
                            None,
                            published_at,
                        )
                        contents.append(content)
                        break

        return sorted(contents, key=lambda content: content.published_at)
