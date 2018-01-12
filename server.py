from os import listdir
from os.path import isfile, join

from bottle import app, route, get, post, request, run, static_file, response
from bson.json_util import dumps
from pymongo import MongoClient
from jinja2 import Environment, FileSystemLoader


jinja2_env = Environment(loader=FileSystemLoader('views/'), cache_size=0)


def template(name, ctx):
    t = jinja2_env.get_template(name + ".tpl")
    return t.render(**ctx)


with open('./get_data/articles.txt') as f:
    articles = f.read().splitlines()

imgs = {}
for article in articles:
    imagefiles = [f for f in listdir('./static/img/articles/' + article) if
                  isfile(join('./static/img/articles/' + article, f))]
    imgs[article] = imagefiles

client = MongoClient()
db = client.test_db
collection = db.test_collection


@route('/')
def index():
    return template('index', {'articles': articles})


@get('/network')
def network():
    node_data = collection.find_one({"label": request.query.search})
    return template('network', {'node_data': dumps(node_data), 'imgs': dumps(imgs)})


@post('/network/expand')
def expand():
    print(request.forms.search)
    node_data = collection.find_one({"label": request.forms.search})
    print("Servring " + node_data["label"])
    return dumps(node_data)


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')


run(host='localhost', port=8000, debug=True)
