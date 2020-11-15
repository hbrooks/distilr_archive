import json
import logging
from pprint import pprint

from .distilr_JSON_serializer import DistilrJsonSerializer

LOG = logging.getLogger(__name__)

from .db_models import ConceptsRow

class Timeline:

    N_EVENTS_PER_DAY = 2
    N_CONCEPTS_PER_DAY = 5

    def __init__(self, id, created_at, time_start, time_end, topic_concept, raw_content=None, processed_content=None):
        self.id = id
        self.created_at = created_at
        self.time_end = time_end
        self.time_start = time_start
        self.topic_concept = topic_concept
        if processed_content != None:
            temp_content = {}
            for k, v in processed_content.items():
                temp_content[DistilrJsonSerializer.string_to_dt(k)] = {
                    "events": [Event.from_dict(e) for e in v["events"]],
                    "concepts": [Concept.from_dict(c) for c in v["concepts"]]
                }
            self.content = temp_content
        else:
            self.content = {}
            temp_content = {}
            
            for raw_event in raw_content:
                published_at = raw_event.published_at
                if published_at not in temp_content:
                    temp_content[published_at] = {
                        "events": [],
                        "concepts": [],
                    }
                temp_content[published_at]["events"].append(raw_event)
                temp_content[published_at]["concepts"].extend(raw_event.concepts)

            for dt, data in temp_content.items():
                allowed_concept_uris = set()
                eligible_concepts = set()
                for c in data["concepts"]:
                    if c.uri not in allowed_concept_uris and c.uri != self.topic_concept.uri:
                        allowed_concept_uris.add(c.uri)
                        eligible_concepts.add(c)
                ordered_events = sorted(data["events"], key = lambda e: e.wgt, reverse=True)
                ordered_concepts = sorted(eligible_concepts, key = lambda c: c.score, reverse=True)
                n_concepts = min(self.N_CONCEPTS_PER_DAY, len(data["events"]))
                self.content[dt] = {
                    "events": ordered_events[:self.N_EVENTS_PER_DAY],
                    "concepts": ordered_concepts[:n_concepts]
                }


    def to_json(self):
        dictionary = {
            'id': self.id,
            "topicConcept": self.topic_concept.to_dict(),
            "timeStart": DistilrJsonSerializer.dt_to_string(self.time_start),
            "timeEnd": DistilrJsonSerializer.dt_to_string(self.time_end),
            'content': self.content_to_dict()
        }
        return json.dumps(dictionary)

    def content_to_dict(self):
        d = {}
        for dt, val in self.content.items():
            d[DistilrJsonSerializer.dt_to_string(dt)] = {
                "events": [e.to_dict() for e in val["events"]],
                "concepts": [c.to_dict() for c in val["concepts"]]
            }
        return d


class Concept:
    def __init__(self, uri, type, score, label):
        self.type = type
        self.label = label
        self.uri = uri
        self.score = score


    def save(self, session):
        session.add(ConceptsRow(
            uri=self.uri,
            type=self.type,
            label=self.label
        ))

    @staticmethod
    def from_uri(session, uri):
        concepts_row = session.query(ConceptsRow).\
            filter(ConceptsRow.uri == uri).\
            first()
        if concepts_row == None:
            return None
        return Concept._build_concept_from_concept_row(concepts_row)


    @staticmethod
    def _build_concept_from_concept_row(row):
        return Concept(
            row.uri,
            row.type,
            None,
            row.label
        )

    def to_dict(self):
        d = {
            'type': self.type,
            'label': self.label,
            'uri': self.uri,
            'score': self.score,
        }
        return d

    @staticmethod
    def from_dict(d):
        return Concept(
            d['uri'],
            d['type'],
            d['score'],
            d['label'],
        )


class Event:
    def __init__(self, published_at, concepts, summary, title, uri, wgt, article):
        self.published_at = published_at
        self.concepts = concepts
        self.summary = summary
        self.title = title
        self.uri = uri
        self.wgt = wgt
        self.article = article

    def to_dict(self):
        d = {
            'summary': self.summary,
            'title': self.title,
            'uri': self.uri,
            'wgt': self.wgt,
            'publishedAt': DistilrJsonSerializer.dt_to_string(self.published_at),
            'article': self.article.to_dict() if self.article != None else None
        }
        return d

    @staticmethod
    def from_dict(d):
        return Event(
            DistilrJsonSerializer.string_to_dt(d['publishedAt']),
            d.get('concepts', []),
            d['summary'],
            d['title'],
            d['uri'],
            d['wgt'],
            Article.from_dict(d['article']),
        )


class Article:
    def __init__(self, uri, url, title, body, categories, concepts):
        self.uri = uri
        self.url = url
        self.title = title
        self.body = body
        self.categories = categories
        self.concepts = concepts

    def to_dict(self):
        return {
            'uri': self.uri,
            'url': self.url,
            'title': self.title,
            'body': self.body,
            'categories': self.categories,
            'concepts': self.concepts
        }

    @staticmethod
    def from_dict(d):
        if d == None:
            return None
        return Article(
            d['uri'],
            d['url'],
            d['title'],
            d['body'],
            d['categories'],
            d['concepts'],
        )
        