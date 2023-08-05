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
import logging
import random
import time
import traceback
from datetime import datetime as dt
from threading import Thread

from redis.lock import Lock

from agora.stoa.actions.core import AGENT_ID
from agora.stoa.client import get_query_generator
from agora.stoa.daemons.delivery import build_response
from agora.stoa.server import app
from agora.stoa.store import r
from agora.stoa.store.tables import db
from agora.stoa.store.triples import fragments_cache
from concurrent.futures.thread import ThreadPoolExecutor

__author__ = 'Fernando Serena'

log = logging.getLogger('agora.curator.daemons.fragment')
AGORA = app.config['AGORA']
BROKER = app.config['BROKER']
ON_DEMAND_TH = float(app.config.get('PARAMS', {}).get('on_demand_threshold', 2.0))
MIN_SYNC = int(app.config.get('PARAMS', {}).get('min_sync_time', 10))
MAX_CONCURRENT_FRAGMENTS = int(app.config.get('PARAMS', {}).get('max_concurrent_fragments', 8))

fragments_key = '{}:fragments'.format(AGENT_ID)

log.info("""Fragment daemon setup:
                    - On-demand threshold: {}
                    - Minimum sync time: {}
                    - Maximum concurrent fragments: {}""".format(ON_DEMAND_TH, MIN_SYNC,
                                                                 MAX_CONCURRENT_FRAGMENTS))

thp = ThreadPoolExecutor(max_workers=min(8, MAX_CONCURRENT_FRAGMENTS))

log.info('Cleaning fragment locks...')
fragment_locks = r.keys('{}:*lock*'.format(fragments_key))
for flk in fragment_locks:
    r.delete(flk)

log.info('Cleaning fragment pulling flags...')
fragment_pullings = r.keys('{}:*:pulling'.format(fragments_key))
for fpk in fragment_pullings:
    r.delete(fpk)


def fragment_lock(fid):
    """
    :param fid: Fragment id
    :return: A redis-based lock object for a given fragment
    """
    lock_key = '{}:{}:lock'.format(fragments_key, fid)
    return r.lock(lock_key, lock_class=Lock)


def __notify_completion(sinks):
    """
    Notify the ending of a fragment collection to all related requests
    :param sinks: Set of dependent sinks
    :return:
    """

    for sink in sinks.values():
        if sink.delivery == 'accepted':
            sink.delivery = 'ready'


def __load_fragment_requests(fid):
    """
    Load all requests and their sinks that are related to a given fragment id
    :param fid: Fragment id
    :return: A dictionary of sinks of all fragment requests
    """
    sinks_ = {}
    fragment_requests_key = '{}:{}:requests'.format(fragments_key, fid)
    for rid in r.smembers(fragment_requests_key):
        try:
            sinks_[rid] = build_response(rid).sink
        except Exception, e:
            traceback.print_exc()
            log.warning(e.message)
            with r.pipeline(transaction=True) as p:
                p.multi()
                p.srem(fragment_requests_key, rid)
                p.execute()
    return sinks_


def __pull_fragment(fid):
    fragment_key = '{}:{}'.format(fragments_key, fid)

    tps = r.smembers('{}:gp'.format(fragment_key))
    r_sinks = __load_fragment_requests(fid)
    log.info("""Starting collection of fragment {}:
                    - GP: {}
                    - Supporting: ({}) {}""".format(fid, list(tps), len(r_sinks), list(r_sinks.keys())))

    try:
        prefixes, gen = get_query_generator(*tps,
                                            broker_host=BROKER['host'],
                                            agora_host=AGORA['host'],
                                            broker_port=BROKER['port'],
                                            agora_port=AGORA['port'], wait=True)
    except Exception, e:
        traceback.print_exc()
        log.error('Scholar is not available')
        return

    lock = fragment_lock(fid)
    lock.acquire()

    with r.pipeline(transaction=True) as p:
        p.multi()
        p.set('{}:pulling'.format(fragment_key), True)
        p.execute()

    db[fid].delete_many({})
    db.drop_collection(fid)

    lock.release()

    try:
        for headers, row in gen:
            try:
                lock.acquire()
                db[fid].insert_one(row)
            except Exception, e:
                log.warning(e.message)
                traceback.print_exc()
            finally:
                lock.release()
    except Exception, e:
        log.error(e.message)

    lock.acquire()
    try:
        with r.pipeline(transaction=True) as p:
            p.multi()
            sync_key = '{}:sync'.format(fragment_key)
            # Fragment is now synced
            p.set(sync_key, True)
            min_durability = int(MIN_SYNC)
            durability = random.randint(min_durability, min_durability * 2)
            p.expire(sync_key, durability)
            log.info('Fragment {} is considered synced for {} s'.format(fid, durability))
            p.set('{}:updated'.format(fragment_key), dt.now())
            p.delete('{}:pulling'.format(fragment_key))
            p.execute()
        if r.scard('{}:requests'.format(fragment_key)) != len(r_sinks):
            r_sinks = __load_fragment_requests(fid)
        __notify_completion(r_sinks)
    finally:
        lock.release()


def __collect_fragments():
    registered_fragments = r.scard(fragments_key)
    synced_fragments = len(r.keys('{}:*:sync'.format(fragments_key)))
    log.info("""Collector daemon started:
                    - Fragments: {}
                    - Synced: {}""".format(registered_fragments, synced_fragments))

    futures = {}
    while True:
        for fid in filter(
                lambda x: r.get('{}:{}:sync'.format(fragments_key, x)) is None and r.get(
                    '{}:{}:pulling'.format(fragments_key, x)) is None,
                r.smembers(fragments_key)):
            if fid in futures:
                if futures[fid].done():
                    del futures[fid]
            if fid not in futures:
                futures[fid] = thp.submit(__pull_fragment, fid)
        time.sleep(1)


def fragment_updated_on(fid):
    return r.get('{}:{}:updated'.format(fragments_key, fid))


def fragment_on_demand(fid):
    return r.get('{}:{}:on_demand'.format(fragments_key, fid))


def is_pulling(fid):
    return r.get('{}:{}:pulling'.format(fragments_key, fid)) is not None


def is_fragment_synced(fid):
    return fragment_updated_on(fid) is not None


def fragment_graph(fid):
    return cache.get_context('/' + fid)


th = Thread(target=__collect_fragments)
th.daemon = True
th.start()
