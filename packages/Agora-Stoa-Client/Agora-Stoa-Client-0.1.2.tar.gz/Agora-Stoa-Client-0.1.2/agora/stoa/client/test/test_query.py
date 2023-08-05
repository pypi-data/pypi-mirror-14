from rdflib import Graph, URIRef
from rdflib.term import Node
from rdflib.namespace import Namespace
from StringIO import StringIO
import networkx as nx
from shortuuid import uuid

SCM = Namespace('http://www.smartdeveloperhub.org/vocabulary/scm#')

g = Graph()

with open('fragment.ttl') as ttl:
    g.parse(StringIO(ttl.read()), format='n3')


def printable(x):
    if isinstance(x, Node):
        return x.toPython()
    return x


def tp_parts(tp):
    """
    :param tp: A triple pattern string
    :return: A string-based 3-tuple like (subject, predicate, object)
    """
    if tp.endswith('"'):
        parts = [tp[tp.find('"'):]]
        st = tp.replace(parts[0], '').rstrip()
        parts = st.split(" ") + parts
    else:
        parts = tp.split(' ')
    return tuple(parts)


def __transform(x):
    """
    Trick to avoid literal language tags problem, etc.
    """
    if x.startswith('"'):
        var = uuid()
        return '?%s FILTER(str(?%s) = %s)' % (var, var, x)
    return x


def build_query(gp, projection):
    def __build_query_from(x, depth=0):
        def build_pattern_query((u, v, data)):
            return '\n%sOPTIONAL { %s %s %s %s }' % ('\t' * (depth + 1), u, data['predicate'], v,__build_query_from(v, depth + 1))
            # if gp_graph.out_degree(v) == 0:
            #     return '\n%sOPTIONAL { %s %s %s}' % ('\t' * (depth + 1), u, data['predicate'], v)
            # else:
            #     x_query = '\n%s%s %s %s %s .' % (
            #         '\t' * (depth + 1), u, data['predicate'], v, __build_query_from(v, depth + 1))
            #     x_query = '\n%sOPTIONAL { %s \n%s}' % ('\t' * (depth + 1), x_query, '\t' * depth)
            #     return x_query

        print depth
        out_edges = list(gp_graph.out_edges_iter(x, data=True))
        out_edges = reversed(sorted(out_edges, key=lambda x: gp_graph.out_degree))
        if out_edges:
            return ' '.join([build_pattern_query(x) for x in out_edges])
        return ''

    gp = filter(lambda x: ' a ' not in x and 'rdf:type' not in x, gp)
    gp_parts = [[__transform(part) for part in tp_parts(tp)] for tp in gp]

    blocks = []
    gp_graph = nx.DiGraph()
    filter_block = []
    for gp_part in gp_parts:
        if 'FILTER' not in gp_part[2]:
            gp_graph.add_edge(gp_part[0], gp_part[2], predicate=gp_part[1])
        else:
            filter_block.append(' '.join(gp_part))

    roots = filter(lambda x: gp_graph.in_degree(x) == 0, gp_graph.nodes())

    blocks += [' %s a agora:Root \n OPTIONAL { %s } .' % (root, __build_query_from(root)) for root in roots]
    if filter_block:
        blocks.append('{ %s }' % ' .\n '.join(filter_block))

    where_gp = ' .\n'.join(blocks)
    query = """SELECT DISTINCT %s WHERE {\n%s\n}""" % (projection, where_gp)
    return query


# qr = g.query("""SELECT ?rn ?bn ?cid ?c ?s ?b WHERE {
#                     {
#                         OPTIONAL { ?s doap:name ?rn }
#                         OPTIONAL { ?s scm:hasBranch ?b
#                             OPTIONAL { ?b doap:name ?bn }
#                             OPTIONAL { ?b scm:hasCommit ?c
#                                 OPTIONAL { ?c scm:commitId ?cid }
#                             }
#                         }
#                     }
#                 }""")

# query = """SELECT DISTINCT ?rn ?bn ?s ?b WHERE {
#                     OPTIONAL {
#                         ?s scm:hasBranch ?b
#                             OPTIONAL {
#                                 ?b doap:name ?bn
#                             }
#                             OPTIONAL {
#                                 ?b scm:hasCommit ?c
#                                 OPTIONAL {
#                                     ?c scm:commitId ?cid
#                                 }
#                             }
#                         OPTIONAL { ?s doap:name ?rn }
#                     }
#                 }"""

# query = """SELECT DISTINCT ?n ?fc ?nk ?d ?r ?b WHERE {
# 	?r a agora:Root
# 	OPTIONAL {
# 		OPTIONAL { ?r scm:hasBranch ?b }
# 		OPTIONAL { ?r doap:developer ?d OPTIONAL { ?d scm:firstCommit ?fc } OPTIONAL { ?d foaf:nick ?nk } }
# 		OPTIONAL { ?r doap:name ?n }
# 	} .
# }"""

query = build_query(
    [
        '?r doap:name ?rn',
        '?r doap:developer ?d',
        '?d foaf:nick ?nk',
        '?d scm:firstCommit ?fc',
        '?r scm:hasBranch ?b'
    ], '?r ?d ?b ?rn ?nk ?fc')
print query

qr = g.query(query)
for r in qr:
    print map(printable, r)
