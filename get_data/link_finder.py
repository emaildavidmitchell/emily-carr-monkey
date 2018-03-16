from SPARQLWrapper import SPARQLWrapper, JSON
from pymongo import MongoClient
from json import dumps
from pprint import pprint


def get_0_degree(l1, l2):
    query = "select distinct ?l1 ?p ?l2 where {?s ?p ?o . ?s rdfs:label ?l1 . " \
            " ?o rdfs:label ?l2 . ?s rdfs:label '" + l1 + "'@en . ?o rdfs:label '" + l2 + \
            "'@en FILTER (lang(?l1) = 'en') FILTER (lang(?l2) = 'en')} LIMIT 2"
    #FILTER (?p != dbo:wikiPageWikiLink)
    data = ex_query(query)
    edges = []
    for link in data['results']['bindings']:
        ret_val = parse_link(link)
        if ret_val != None:
            edges.append(ret_val)
    return edges

def get_1_degree(l1, l2):
    query = "select distinct ?l1 ?p1 ?l2 ?p2 ?l3  where {?s ?p1 ?i1 . ?i1 ?p2 ?o . ?s rdfs:label ?l1 . " \
            "?i1 rdfs:label ?l2 . ?o rdfs:label ?l3 . ?s rdfs:label '" + l1 + "'@en . ?o rdfs:label '" \
            + l2 + "'@en FILTER (lang(?l1) = 'en') FILTER (lang(?l2) = 'en') FILTER (lang(?l3) = 'en')} LIMIT 2"
    #"FILTER (?p1 != dbo:wikiPageWikiLink) FILTER (?p2 != dbo:wikiPageWikiLink)}"

    data = ex_query(query)
    edges = []
    for link in data['results']['bindings']:
        ret_val = parse_link(link)
        if ret_val != None:
            edges.append(ret_val)
    return edges

def get_2_degree(l1, l2):
    query = "select distinct ?l1 ?p1 ?l2 ?p2 ?l3 ?p3 ?l4 where {?s ?p1 ?i1 . ?i1 ?p2 ?i2 . ?i2 ?p3 ?o ." \
            "?s rdfs:label ?l1 . ?i1 rdfs:label ?l2 . ?i2 rdfs:label ?l3 . ?o rdfs:label ?l4 . ?s rdfs:label '" \
            + l1 + "'@en . ?o rdfs:label '" + l2 + "'@en FILTER (lang(?l1) = 'en') FILTER (lang(?l2) = 'en') " \
            "FILTER (lang(?l3) = 'en') FILTER (lang(?l4) = 'en') FILTER (?p2 != dbo:wikiPageWikiLink)} LIMIT 2 "
    data = ex_query(query)
    edges = []
    for link in data['results']['bindings']:
        ret_val = parse_link(link)
        if ret_val != None and l1 not in ret_val[2:] and l2 not in ret_val[:-1]:
            edges.append(ret_val)
    return edges

def parse_link(link):
    edge = []
    for key in link:
        if "sameAs" in link[key]['value'] or "wikidata" in link[key]['value']:
            return None
        edge.append(link[key]['value'])
    return edge

def ex_query(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    return sparql.query().convert()
