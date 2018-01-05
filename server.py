from bottle import route, get, post, request, run, static_file, jinja2_template as template
from pymongo import MongoClient

with open('./get_data/articles.txt') as f:
	articles = f.read().splitlines()
	articles = [article for article in articles]

client = MongoClient()
db = client.test_db
collection = db.test_collection

@route('/')
def index():
  return template('index',articles=articles)

@get('/network')
def network():
    node_data = collection.find_one({"label": request.query.search})
    return template('network',node_data=node_data)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')


run(host='localhost', port=8000, debug=True)

