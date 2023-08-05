from elasticsearch import Elasticsearch as _Elasticsearch

from docido_sdk.core import (
    Component,
    implements,
)
from docido_sdk.index import (
    IndexAPIProcessor,
    IndexAPIProvider,
)
import docido_sdk.config as docido_config

import os

__all__ = ['Elasticsearch', 'ElasticsearchMapping']

ES_BULK_OPERATION = ['index', 'create', 'update', 'delete']


class ElasticsearchMappingProcessor(IndexAPIProcessor):
    def __init__(self, **config):
        super(ElasticsearchMappingProcessor, self).__init__(**config)
        self.update_mapping(config['service'])

    def update_mapping(self, service):
        config = docido_config.elasticsearch
        es = _Elasticsearch(
            os.getenv('ELASTICSEARCH_HOST', config.ES_HOST),
            **config.get('connection_params', {})
        )
        to_update_mappings = [
            (config.ES_INDEX, config.ES_CARD_TYPE),
        ]
        if config.get('ES_STORE_INDEX') and config.get('ES_STORE_TYPE'):
            to_update_mappings.append(
                (config.ES_STORE_INDEX, config.ES_STORE_TYPE)
            )
        for (index, doc_type) in to_update_mappings:
            self.__update_index_mapping(es, service, index, doc_type)

    @classmethod
    def __get_crawler_mapping_config(cls, service):
        pr_config = docido_config.get('pull_crawlers', {})
        crawlers_config = pr_config.get('crawlers', {})
        crawler_config = crawlers_config.get(service, {})
        crawler_index_config = crawler_config.get('indexing', {})
        crawler_es = crawler_index_config.get('elasticsearch', {})
        return crawler_es.get('mapping', {})

    def __update_index_mapping(self, es, service, index, doc_type):
        config = docido_config.elasticsearch
        index = index.format(service=service)
        doc_type = doc_type.format(service=service)
        if not es.indices.exists(index):
            es.indices.create(index)
        mappings = []
        if 'MAPPING' in config:
            if index in config.MAPPING:
                mappings.append(config.MAPPING[index])
        crawler_mapping = self.__get_crawler_mapping_config(service)
        if any(crawler_mapping):
            mappings.append(crawler_mapping)
        for mapping in mappings:
            for field in mapping.keys():
                mapping_update_response = es.indices.put_mapping(
                    index=index,
                    doc_type=doc_type,
                    body=mapping[field]
                )
                if mapping_update_response != {'acknowledged': True}:
                    raise Exception("Could not update mapping")


class ElasticsearchProcessor(IndexAPIProcessor):
    """ Main Elasticsearch entry point

    Every sent card or thumbnail will get indexed in the user's associated
    index.

    Also provide convenience method for documents search and deletion
    """

    def __init__(self, **config):
        super(ElasticsearchProcessor, self).__init__(**config)
        es_config = docido_config.elasticsearch
        service = config['service']
        fmt = {'service': service}
        self.__es_index = es_config.ES_INDEX.format(**fmt)
        self.__es_store_index = es_config.ES_STORE_INDEX.format(**fmt)
        self.__card_type = es_config.ES_CARD_TYPE.format(**fmt)
        self.__store_type = es_config.ES_STORE_TYPE.format(**fmt)
        self.__routing = config.get('elasticsearch', {}).get('routing')
        self.__es = _Elasticsearch(
            os.getenv('ELASTICSEARCH_HOST', es_config.ES_HOST),
            **es_config.get('connection_params', {})
        )
        self.__es_store = _Elasticsearch(
            os.getenv('ELASTICSEARCH_HOST', es_config.ES_HOST),
            **es_config.get('connection_params', {})
        )

    def ping(self):
        return self.__es.ping() and self.__es_store.ping()

    def search_cards(self, query):
        generated_results = 0
        batch_size = 10
        offset = 0
        body = {
            'body': query,
            'index': self.__es_index,
            'doc_type': self.__card_type,
            'size': batch_size,
            'from_': offset,
        }
        if self.__routing:
            body['routing'] = self.__routing
        search_results = self.__es.search(**body)

        while generated_results != search_results['hits']['total']:
            for hit in search_results['hits']['hits']:
                generated_results += 1
                yield hit['_source']

            offset += batch_size
            body['from_'] = offset
            search_results = self.__es.search(**body)

    def __delete_es_docs(self, body, es, index, doc_type):
        query = {
            'body': body,
            'index': index,
            'doc_type': doc_type,
        }
        if self.__routing:
            query['routing'] = self.__routing
        es.delete_by_query(**query)

    def delete_cards(self, query):
        return self.__delete_es_docs(
            query,
            self.__es,
            self.__es_index,
            self.__card_type
        )

    def delete_cards_by_id(self, ids):
        return self.__delete_by_id(ids, self.__es_index, self.__card_type)

    def delete_thumbnails(self, query):
        return self.__delete_es_docs(
            query,
            self.__es_store,
            self.__es_store_index,
            self.__store_type
        )

    def delete_thumbnails_by_id(self, ids):
        return self.__delete_by_id(ids, self.__es_store_index,
                                   self.__store_type)

    def __delete_by_id(self, ids, index, _type):
        error_docs = []
        body = [{
            'delete': {
                '_index': index,
                '_type': _type,
                '_id': _id
            }
        } for _id in ids]

        if not any(body):
            return error_docs

        params = {
            'body': body,
            'refresh': True,
        }
        if self.__routing:
            params['routing'] = self.__routing

        results = self.__es.bulk(**params)
        for index, result in enumerate(results['items']):
            if result['delete']['status'] is not 200:
                error_docs.append({
                    'status': result['delete']['status'],
                    'id': ids[index],
                })
        return error_docs

    def __push_es_docs(self, docs, es, index, doc_type):
        body = []
        error_docs = []

        for doc in docs:
            action = {
                'index': {
                    '_index': index,
                    '_type': doc_type
                }
            }
            body.append(action)
            body.append(doc)

        if len(body) == 0:
            return error_docs

        params = {
            'body': body,
            'refresh': True,
        }
        if self.__routing:
            params['routing'] = self.__routing

        results = es.bulk(**params)
        if results['errors']:
            for index, item in enumerate(results['items']):
                for operation in ES_BULK_OPERATION:
                    if operation in item:
                        if item[operation]['status'] not in [200, 201]:
                            error_docs.append({
                                'card': docs[index],
                                'status': item[operation]['status'],
                                'id': docs[index]['id']
                                if 'id' in docs[index] else None,
                                'error': item[operation]['error'],
                            })
                            break
        return error_docs

    def push_cards(self, cards):
        return self.__push_es_docs(
            cards,
            self.__es,
            self.__es_index,
            self.__card_type
        )

    def push_thumbnails(self, thumbnails):
        return self.__push_es_docs(
            [
                {
                    'id': t[0],
                    'content': {
                        'data': t[1],
                        'mimetype': t[2]
                    }
                }
                for t in thumbnails],
            self.__es_store,
            self.__es_store_index,
            self.__store_type
        )


class Elasticsearch(Component):
    implements(IndexAPIProvider)

    def get_index_api(self, **config):
        return ElasticsearchProcessor(**config)


class ElasticsearchMapping(Component):
    implements(IndexAPIProvider)

    def get_index_api(self, **config):
        return ElasticsearchMappingProcessor(**config)
