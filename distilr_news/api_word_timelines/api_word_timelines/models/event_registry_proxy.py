from pprint import pprint
import datetime
import logging

import requests
from eventregistry import *

from .timeline import Event
from .timeline import Concept
from .timeline import Article
from ..exceptions import NotEnoughDataToCreateTimeline

LOG = logging.getLogger(__name__)


# 10 cents per timeline.

class NoDataFound(Exception):
    pass


class EventRegistryApiProxy:

    RETURN_INFO = ReturnInfo(
        articleInfo=ArticleInfoFlags(
            bodyLen=-1,
            basicInfo=True,
            title=True,
            body=True,
            url=True,
            eventUri=False,
            authors=False,
            concepts=True,
            categories=True,
            links=False,
            videos=False,
            image=False, # TODO:
            socialScore=False,
            sentiment=False,
            location=False,
            dates=False,
            extractedDates=False,
            originalArticle=False, # The metiod hopefully isn't a duplicate...
            storyUri=False
        ),
        eventInfo=EventInfoFlags(
            title=True,
            summary=True,
            articleCounts=True,
            concepts=True,
            categories=False, # TODO: Be able to build timelines from these.
            location=False,
            commonDate=False,
            infoArticle=False,
            stories=True,
            socialScore=False,
            imageCount=0
        ),
        conceptInfo=ConceptInfoFlags(
            synonyms=False,
            image=False,
            description=False,
        ),
        storyInfo=StoryInfoFlags(
            basicStats=True,
            location=False,
            date=False,
            title=True,
            summary=True,
            concepts=False,
            categories=False,
            medoidArticle=True,
            infoArticle=False,
            commonDates=False,
            socialScore=False,
            imageCount=0
        ),
    )

    REQUEST_EVENTS_INFOS = RequestEventsInfo(
        page = 1,
        count = 50,
        sortBy = "rel",
        sortByAsc = False,
        returnInfo = RETURN_INFO
    )


    def __init__(self, api_key):
        self.api_key = api_key
        self.er = EventRegistry(
            apiKey=self.api_key,
            allowUseOfArchive=False,
        )


    def get_concept(self, query_string):
        results = self.er.suggestConcepts(query_string, lang="eng")
        if results == None or len(results) == 0:
            return None
        result = results[0]
        return Concept(
            result['uri'],
            result['type'],
            None,
            result['label']['eng']
        )


    def get_events_from_query(self, query, dt_start, dt_end):
        query = QueryEvents(
            keywords=query,
            lang='eng',
            dateStart=dt_start,
            dateEnd=dt_end,
            minArticlesInEvent=5,
            requestedResult=self.REQUEST_EVENTS_INFOS
        )
        response_body = self._execute_query(query)
        return self._format_events(response_body)
        
        
    def _format_events(self, response_events):
        events = []
        for e in response_events:
            concepts = []
            for c in e['concepts'][:10]: # These are ordered by score.
                concepts.append(Concept(
                    c['uri'],
                    c['type'],
                    c['score'],
                    c['label']['eng']
                ))
            article = None
            if 'stories' in e and len([e['stories']]) > 0:
                story = e['stories'][0]
                if 'mediodArticle' in story:
                    mediod_article = story['mediodArticle']
                    article = Article(
                        mediod_article['uri'],
                        mediod_article['url'],
                        mediod_article['title'],
                        mediod_article['body'],
                        mediod_article['categories'],
                        mediod_article['concepts']
                    )
            event = Event(
                datetime.datetime.strptime(e['eventDate'], '%Y-%m-%d'),
                concepts,
                e['summary']['eng'],
                e['title']['eng'],
                e['uri'],
                e['wgt'],
                article
            )
            events.append(event)
        return events
        

    def get_events_from_uri(self, uri, dt_start, dt_end):
        query = QueryEvents(
            conceptUri=uri,
            lang='eng',
            dateStart=dt_start,
            dateEnd=dt_end,
            minArticlesInEvent=5,
            requestedResult=self.REQUEST_EVENTS_INFOS
        )
        response_body = self._execute_query(query)
        return self._format_events(response_body)


    def _execute_query(self, query):
        query_results = self.er.execQuery(query)
        events = query_results['events']
        if events['count'] <= 0:
            raise NotEnoughDataToCreateTimeline()
        return events['results']

    def fetch_trending_concepts(self):
        query_parameters = {
            "conceptType": [
                "person",
                "org",
                "loc",
            ],
            "source": "news",
            "conceptCount": 20,
            "apiKey": self.api_key,
        }
        r = requests.request(
            url="http://eventregistry.org/api/v1/trends/getConceptTrendGroups",
            method='get',
            params=query_parameters
        )
        r.raise_for_status()
        return r.json()
        