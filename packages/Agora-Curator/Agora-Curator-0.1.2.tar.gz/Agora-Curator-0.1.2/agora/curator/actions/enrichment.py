"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  This file is part of the Smart Developer Hub Project:
    http://www.smartdeveloperhub.org

  Center for Open Middleware
        http://www.centeropenmiddleware.com/
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Copyright (C) 2015 Center for Open Middleware.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at 

            http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
"""
import base64
import calendar
import logging
import traceback
import uuid
from datetime import datetime

from agora.curator.daemons.fragment import is_fragment_synced, fragment_lock
from agora.stoa.actions.core import STOA, TYPES, RDF, XSD, FOAF, AGENT_ID
from agora.stoa.actions.core.delivery import LIT_AGENT_ID
from agora.stoa.actions.core.fragment import FragmentRequest, FragmentAction, FragmentResponse, FragmentSink
from agora.stoa.actions.core.utils import CGraph, GraphPattern
from agora.stoa.store import r
from agora.stoa.store.tables import db
from rdflib import BNode, Literal, URIRef
from shortuuid import uuid as suuid

__author__ = 'Fernando Serena'

log = logging.getLogger('agora.curator.actions.enrichment')


enrichments_key = '{}:enrichments'.format(AGENT_ID)


def get_fragment_enrichments(fid):
    return [EnrichmentData(eid) for eid in r.smembers('{}:fragments:{}:enrichments'.format(AGENT_ID, fid))]


def generate_enrichment_hash(target, links):
    links = '|'.join(sorted([str(pr) for (pr, _) in links]))
    eid = base64.b64encode('~'.join([target, links]))
    return eid


def register_enrichment(pipe, fid, target, links):
    e_hash = generate_enrichment_hash(target, links)
    if not r.sismember(enrichments_key, e_hash):
        eid = suuid()
        enrichment_data = EnrichmentData(eid, fid, target, links)
        enrichment_data.save(pipe)
        pipe.sadd(enrichments_key, e_hash)
        pipe.set('{}:map:enrichments:{}'.format(AGENT_ID, e_hash), eid)
    else:
        eid = r.get('{}:map:enrichments:{}'.format(AGENT_ID, e_hash))
    return eid


class EnrichmentData(object):
    def __init__(self, eid, fid=None, target=None, links=None):
        if eid is None:
            raise ValueError('Cannot create an enrichment data object without an identifier')

        self.links = links
        if target is not None:
            self.target = URIRef(target)
        self.target = target
        self.fragment_id = fid
        self.enrichment_id = eid
        self._enrichment_key = '{}:enrichments:{}'.format(AGENT_ID, self.enrichment_id)

        if not any([fid, target, links]):
            self.load()

    def save(self, pipe):
        pipe.hset('{}'.format(self._enrichment_key), 'target', self.target)
        pipe.hset('{}'.format(self._enrichment_key), 'fragment_id', self.fragment_id)
        pipe.sadd('{}:fragments:{}:enrichments'.format(AGENT_ID, self.fragment_id), self.enrichment_id)
        pipe.sadd('{}:links'.format(self._enrichment_key), *map(lambda x: str(x), self.links))
        pipe.hmset('{}:links:status'.format(self._enrichment_key),
                   dict((pr, False) for (pr, _) in self.links))

    def load(self):
        dict_fields = r.hgetall(self._enrichment_key)
        self.target = URIRef(dict_fields.get('target', None))
        self.fragment_id = dict_fields.get('fragment_id', None)
        self.links = map(lambda (link, v): (URIRef(link), v), [eval(pair_str) for pair_str in
                                                               r.smembers('{}:links'.format(
                                                                   self._enrichment_key))])

    def set_link(self, link):
        with r.pipeline(transaction=True) as p:
            p.multi()
            p.hset('{}:links:status'.format(self._enrichment_key), str(link), True)
            p.execute()

    @property
    def completed(self):
        return all([eval(value) for value in r.hgetall('{}:links:status'.format(self._enrichment_key)).values()])


class EnrichmentRequest(FragmentRequest):
    def __init__(self):
        super(EnrichmentRequest, self).__init__()
        self._target_resource = None
        self._target_links = set([])

    def _extract_content(self, request_type=STOA.EnrichmentRequest):
        super(EnrichmentRequest, self)._extract_content(request_type)

        q_res = self._graph.query("""SELECT ?node ?t WHERE {
                                        ?node a stoa:EnrichmentRequest;
                                              stoa:targetResource ?t
                                    }""")

        q_res = list(q_res)
        if len(q_res) != 1:
            raise SyntaxError('Invalid enrichment request')

        request_fields = q_res.pop()
        if not all(request_fields):
            raise ValueError('Missing fields for enrichment request')
        if request_fields[0] != self._request_node:
            raise SyntaxError('Request node does not match')

        (self._target_resource,) = request_fields[1:]

        log.info("""Parsed attributes of an enrichment request:
                    -target resource: {}""".format(self._target_resource))

        target_pattern = self._graph.predicate_objects(self._target_resource)
        for (pr, req_object) in target_pattern:
            if (req_object, RDF.type, STOA.Variable) in self._graph:
                self._target_links.add((pr, req_object))
        enrich_properties = set([pr for (pr, _) in self._target_links])
        if not enrich_properties:
            raise ValueError('There is nothing to enrich')
        log.info(
            """<{}> is requested to be enriched with values for the following properties:
                    {}""".format(
                self._target_resource,
                '\n'.join(enrich_properties)))

        self._graph_pattern = GraphPattern(filter(lambda x: self._target_resource not in x, self._graph_pattern))

    @property
    def target_resource(self):
        return self._target_resource

    @property
    def target_links(self):
        return self._target_links.copy()


class EnrichmentAction(FragmentAction):
    def __init__(self, message):
        self.__request = EnrichmentRequest()
        self.__sink = EnrichmentSink()
        super(EnrichmentAction, self).__init__(message)

    @property
    def sink(self):
        return self.__sink

    @classmethod
    def response_class(cls):
        return EnrichmentResponse

    @property
    def request(self):
        return self.__request

    def submit(self):
        super(EnrichmentAction, self).submit()
        if is_fragment_synced(self.sink.fragment_id):
            self.sink.delivery = 'ready'


class EnrichmentSink(FragmentSink):
    def _remove(self, pipe):
        pipe.srem(enrichments_key, self._request_id)
        super(EnrichmentSink, self)._remove(pipe)

    def __init__(self):
        super(EnrichmentSink, self).__init__()
        self.__target_links = None
        self.__target_resource = None
        self._enrichment_id = None
        self._enrichment_data = None

    def _save(self, action, general=True):
        super(EnrichmentSink, self)._save(action, general)
        variable_links = [(str(pr), self.map(action.request.variable_label(v))) for (pr, v) in
                          action.request.target_links]

        enrichment_id = register_enrichment(self._pipe, self.fragment_id, action.request.target_resource,
                                            variable_links)
        self._pipe.hset('{}'.format(self._request_key), 'enrichment_id', enrichment_id)
        self._dict_fields['enrichment_id'] = enrichment_id

    def _load(self):
        super(EnrichmentSink, self)._load()

    @property
    def enrichment_data(self):
        if self._enrichment_data is None:
            self._enrichment_data = EnrichmentData(self.enrichment_id)
            self._enrichment_data.load()
        return self._enrichment_data

    @property
    def backed(self):
        return self.fragment_updated_on is not None and EnrichmentData(
            self.enrichment_id).completed


class EnrichmentResponse(FragmentResponse):
    def __init__(self, rid):
        self.__sink = EnrichmentSink()
        self.__sink.load(rid)
        self.__fragment_lock = fragment_lock(self.__sink.fragment_id)
        super(EnrichmentResponse, self).__init__(rid)

    @property
    def sink(self):
        return self.__sink

    def build(self):
        self.__fragment_lock.acquire()
        generator = self._build()
        try:
            for response in generator:
                yield response
        except Exception, e:
            traceback.print_exc()
            log.error(e.message)
        finally:
            self.__fragment_lock.release()

    def _build(self):
        log.debug('Building a response for request number {}'.format(self._request_id))
        result = self.result_set()
        enrichment = self.sink.enrichment_data
        object_links = {}

        for res in result:
            links = dict(map(lambda (l, v): (v.lstrip('?'), l), enrichment.links))
            for link in links:
                try:
                    object_link = URIRef(res[link])
                    if links[link] not in object_links:
                        object_links[links[link]] = set([])
                    object_links[links[link]].add(object_link)
                except KeyError:
                    pass

        graph = CGraph()
        resp_node = BNode('#response')
        graph.add((resp_node, RDF.type, STOA.EnrichmentResponse))
        graph.add((resp_node, STOA.messageId, Literal(str(uuid.uuid4()), datatype=TYPES.UUID)))
        graph.add((resp_node, STOA.responseTo, Literal(self.sink.message_id, datatype=TYPES.UUID)))
        graph.add((resp_node, STOA.responseNumber, Literal("1", datatype=XSD.unsignedLong)))
        graph.add((resp_node, STOA.targetResource, self.sink.enrichment_data.target))
        graph.add((resp_node, STOA.submittedOn, Literal(datetime.now())))
        curator_node = BNode('#curator')
        graph.add((resp_node, STOA.submittedBy, curator_node))
        graph.add((curator_node, RDF.type, FOAF.Agent))
        graph.add((curator_node, STOA.agentId, LIT_AGENT_ID))
        addition_node = BNode('#addition')
        graph.add((resp_node, STOA.additionTarget, addition_node))
        graph.add((addition_node, RDF.type, STOA.Variable))
        if object_links:
            for link, v in self.sink.enrichment_data.links:
                [graph.add((addition_node, link, o)) for o in object_links[link]]
        yield graph.serialize(format='turtle'), {'state': 'end', 'source': 'store',
                                                 'response_to': self.sink.message_id,
                                                 'submitted_on': calendar.timegm(datetime.now().timetuple()),
                                                 'submitted_by': self.sink.submitted_by,
                                                 'format': 'turtle'}

        self.sink.delivery = 'sent'

    def result_set(self):
        pattern = {}
        mapping = filter(lambda x: x.startswith('?'), self.sink.mapping)
        for v in mapping:
            value = self.sink.map(v, fmap=True)
            if not value.startswith('?'):
                pattern[v.lstrip('?')] = value.strip('"')

        table = db[self.sink.fragment_id]
        return table.find(pattern)
