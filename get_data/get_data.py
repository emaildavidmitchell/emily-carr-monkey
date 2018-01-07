from SPARQLWrapper import SPARQLWrapper, JSON
from pymongo import MongoClient
from json import dumps
from pprint import pprint

descs = None
with open("./articles.txt") as f:
	articles = f.read().splitlines()


def get_article_data():
	global articles
	client = MongoClient()
	db = client.test_db
	collection = db.test_collection
	collection.remove()
	for article in articles:
		try:
			print(article)
			node = get_node_data(article.replace("'", r"\'"))
			collection.insert_one(node)
		except:
			print("Didnt go so well")
			pass
	client.close()


def get_node_data(label):
	data = {}
	data["label"] = label
	data["source"] = get_source(label)
	data["io"] = get_io(label)
	data["oo"] = get_oo(label)
	data["info"] = get_info(label)
	data["type"] = get_type(label)
	data["desc"] = get_desc(label)
	return data

def get_desc(label):
	global descs
	if descs:
		if label in descs:
			return descs[label]
		else:
			return None
	else:
		with open("./art_desc.txt") as f:
			descs = f.readlines()
			descs = {k:v for k,v in (item.split(":::") for item in descs)}
		if label in descs:
			return descs[label]
		else:
			return None		


def get_source(label):
	source_query = "select distinct ?s where {?s rdfs:label '" + label + "'@en filter regex(?s, 'dbpedia') } LIMIT 1";
	result = ex_query(source_query)
	if len(result['results']['bindings']) > 0:
		return result['results']['bindings'][0]['s']['value']
	else:
		return None

def get_io(label):
	global articles
	io_query = "select distinct ?o ?p ?l where { ?s ?p ?o . ?s rdfs:label '" + label + "'@en . ?p rdf:type owl:ObjectProperty . ?o rdfs:label ?l . filter langMatches(lang(?l),'EN')}";
	result = ex_query(io_query)
	if len(result['results']['bindings']) > 0:
		result = [{'uri': item['o']['value'], 'label': item['l']['value'], 'relation': item['p']['value']} for item in result['results']['bindings'] if item['l']['value'] in articles]
		return result
	else:
		return None

def get_oo(label):
	global articles
	oo_query = "select distinct ?o ?p ?l where { ?s ?p ?o . ?o rdfs:label '" + label + "'@en . ?p rdf:type owl:ObjectProperty . ?s rdfs:label ?l . filter langMatches(lang(?l),'EN')}";
	result = ex_query(oo_query)
	if len(result['results']['bindings']) > 0:
		result = [{'uri': item['o']['value'], 'label': item['l']['value'], 'relation': item['p']['value']} for item in result['results']['bindings'] if item['l']['value'] in articles]
		return result
	else:
		return None

def get_info(label):
	info_query = "select distinct ?o ?p where { ?s ?p ?o . ?s rdfs:label '" + label + "'@en . ?p rdf:type owl:DatatypeProperty }";
	result = ex_query(info_query)
	if len(result['results']['bindings']) > 0:
		return [{'datatype': item['p']['value'],'value': item['o']['value']} for item in result['results']['bindings'] if 'xml:lang' not in item['o']]
	else:
		return None

def get_type(label):
	type_query = "select distinct ?t where {?s rdfs:label '" + label + "'@en . ?s rdf:type ?t } LIMIT 500";
	result = ex_query(type_query)
	if len(result['results']['bindings']) > 0:
		return [item['t']['value'] for item in result['results']['bindings']]
	else:
		return None    

def ex_query(query):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setReturnFormat(JSON)
	sparql.setQuery(query)
	return sparql.query().convert()

get_article_data()

