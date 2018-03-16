import json
from os import listdir
from os.path import isfile, join

from bottle import route, get, post, request, run, static_file
from jinja2 import Environment, FileSystemLoader

from get_data import link_finder

jinja2_env = Environment(loader=FileSystemLoader('views/'), cache_size=0)


def template(name, ctx):
    t = jinja2_env.get_template(name + ".tpl")
    return t.render(**ctx)


with open('./get_data/ak.txt') as f:
    ak = f.read().splitlines()
    ak = [line.split(":::") for line in ak]
    aid = {item[0]: item[1] for item in ak}
    ida = {item[1]: item[0] for item in ak}

with open('./get_data/art_desc.txt') as f:
    desc = f.read().splitlines()
    desc = [line.split(":::") for line in desc]
    desc = {item[0]: item[1] for item in desc if len(item) == 2}

imgs = {}
for article in aid.keys():
    imagefiles = [f for f in listdir('./static/img/articles/' + article) if
                  isfile(join('./static/img/articles/' + article, f))]
    imgs[article] = imagefiles


def proc_edges(edges):
    for i in range(len(edges)):
        edges[i] = list(map(lambda val: aid[val] if val in aid else val, edges[i]))
    return edges


@route('/')
def index():
    return template('index', {'aid': aid, 'ida': ida})


@get('/network')
def network():
    print("Getting network request for " + request.query['search'])
    return template('network',
                    {'aid': aid, 'ida': ida, 'desc': desc, 'imgs': imgs, 's_node': aid[request.query['search']]})


@post('/expand')
def expand():
    add_node = ida[request.forms.add_node]
    ex_nodes = json.loads(request.forms.ex_nodes)
    ex_nodes = list(map(lambda x: ida[x], ex_nodes))
    edges = []
    for ex_node in ex_nodes:
        print("Getting links between " + add_node + " and " + ex_node)
        edges += link_finder.get_0_degree(add_node, ex_node)
        edges += link_finder.get_0_degree(ex_node, add_node)
        edges += link_finder.get_1_degree(add_node, ex_node)
        edges += link_finder.get_1_degree(ex_node, add_node)
        edges += link_finder.get_2_degree(add_node, ex_node)
        edges += link_finder.get_2_degree(ex_node, add_node)

    edges = json.dumps(proc_edges(edges))
    print("Adding node " + str(add_node));

    rv = {'edges': edges, 'add_node': aid[add_node]}
    return rv


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')


run(host='localhost', port=8000, debug=True)
