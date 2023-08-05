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
from datetime import datetime as time

from agora.stoa.client import get_fragment_generator, get_enrichment_generator, get_query_generator
import logging

__author__ = 'Fernando Serena'

ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
logger = logging.getLogger('agora')
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

AGORA_HOST = '138.4.249.224'
AGORA_PORT = 9009

BROKER_HOST = '138.4.249.161'
# AGORA_HOST = '138.4.249.161'
# AGORA_PORT = 9002

# BROKER_HOST = '192.168.1.43'
# AGORA_HOST = '192.168.1.43'
# BROKER_HOST = '138.4.220.50'
# AGORA_HOST = '138.4.220.50'

# prefixes, gen = get_enrichment_generator('?s a dbpedia-owl:Film',
#                                          '?s foaf:name "Alice"',
#                                          '* amovies:hasFilm ?s',
#                                          broker_host=BROKER_HOST,
#                                          agora_host=AGORA_HOST,
#                                          agora_port=9002,
#                                          target='http://localhost:5005/',
#                                          wait=True,
#                                          exchange='sdh',
#                                          topic_pattern='curator.request')

# prefixes, gen = get_enrichment_generator('?s dbpedia-owl:starring ?a',
#                                          '* amovies:hasActor ?a',
#                                          broker_host=BROKER_HOST,
#                                          agora_host=AGORA_HOST,
#                                          agora_port=9002,
#                                          target='http://localhost:5005/',
#                                          wait=True,
#                                          exchange='sdh',
#                                          topic_pattern='curator.request')

# prefixes, gen = get_enrichment_generator('?s a dbpedia-owl:Film',
#                                          '?s foaf:name "2046"',
#                                          '* amovies:hasFilm ?s',
#                                          broker_host=BROKER_HOST,
#                                          agora_host=AGORA_HOST,
#                                          agora_port=AGORA_PORT,
#                                          target='http://localhost:5005/',
#                                          wait=True,
#                                          exchange='sdh',
#                                          topic_pattern='curator.request',
#                                          response_prefix='curator.response')

# prefixes, gen = get_enrichment_generator('?s dbpedia-owl:starring ?a',
#                                          '?a dbp:birthName "Paul Frederic Simon"',
#                                          '* amovies:hasActor ?a',
#                                          broker_host=BROKER_HOST,
#                                          agora_host=AGORA_HOST,
#                                          agora_port=AGORA_PORT,
#                                          target='http://localhost:5005/',
#                                          wait=True,
#                                          exchange='sdh',
#                                          topic_pattern='curator.request',
#                                          response_prefix='curator.response')


# prefixes, gen = get_fragment_generator('?s dbpedia-owl:starring ?a',
#                                        '?s foaf:name "2046"',
#                                        broker_host='138.4.249.164',
#                                        agora_host='138.4.249.164',
#                                        agora_port=9002, wait=True)

# prefixes, gen = get_query_generator('?_s foaf:name "20,000 Leagues Under the Sea"',
#                                        '?_s dbpedia-owl:starring ?a',
#                                        '?a foaf:depiction ?im',
#                                        '?a dbp:birthName ?bn',
#                                        broker_host='192.168.1.43',
#                                        agora_host='192.168.1.43',
#                                        agora_port=9002, wait=True)

# prefixes, gen = get_fragment_generator('<http://dbpedia.org/resource/55_Days_at_Peking> dbpedia-owl:starring ?a',
#                                        '<http://dbpedia.org/resource/55_Days_at_Peking> foaf:name ?n',
#                                        broker_host=BROKER_HOST,
#                                        agora_host=AGORA_HOST,
#                                        agora_port=AGORA_PORT, wait=True)

# prefixes, gen = get_query_generator('?s dbpedia-owl:starring ?a',
#                                        '?a dbp:birthName ?n',
#                                        broker_host=BROKER_HOST,
#                                        agora_host=AGORA_HOST,
#                                        agora_port=AGORA_PORT, wait=True)

# prefixes, gen = get_query_generator('<http://dbpedia.org/resource/55_Days_at_Peking> dbpedia-owl:starring ?a',
#                                        '<http://dbpedia.org/resource/55_Days_at_Peking> foaf:name ?n',
#                                        '?h amovies:hasFilm <http://dbpedia.org/resource/55_Days_at_Peking>',
#                                        broker_host='192.168.1.43',
#                                        agora_host='192.168.1.43',
#                                        agora_port=9002, wait=True)


# prefixes, gen = get_fragment_generator('?s doap:name ?rn', '?s scm:hasBranch ?b', '?b doap:name ?bn', '?b scm:hasCommit ?c',
#                                     '?c scm:commitId ?cid',
#                                     broker_host=BROKER_HOST,
#                                     agora_host=AGORA_HOST,
#                                     agora_port=AGORA_PORT, wait=True)

prefixes, gen = get_enrichment_generator('?r a scm:Repository',
                                         '?r doap:name "sdh-scm-metrics"',
                                         '?r scm:hasBranch ?b',
                                         '?b doap:name "master"',
                                         '?b scm:hasCommit ?c',
                                         '?c scm:commitId "db1aab9fa7aada3c2ef878cc082837c34104ac68"',
                                         '* scm:forCommit ?c',
                                         broker_host=BROKER_HOST,
                                         agora_host=AGORA_HOST,
                                         agora_port=AGORA_PORT,
                                         target='http://localhost:5005/',
                                         wait=True,
                                         exchange='sdh',
                                         topic_pattern='curator.request',
                                         response_prefix='curator.response')

pre = time.now()
for headers, content in gen:
    format = headers.get('format')
    if format == 'turtle':
        print content.serialize(format='turtle')
    else:
        print content
post = time.now()
print 'Elapsed time: {}'.format((post - pre).total_seconds())
