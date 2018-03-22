var id_counter = 1;
var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
var height = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
var nodeIds = [];
var shadowState = false;
var nodesArray = [];
var nodes = new vis.DataSet(nodesArray);
var edgesArray = [];
var edges = new vis.DataSet(edgesArray);
var container = document.getElementById('graph-container');
var img_num = 0;
var img_max = 0;
var data = {
    nodes: nodes,
    edges: edges
}

console.log('test');

var options = {
  edges: {
    smooth: false
  },
  physics: {
    forceAtlas2Based: {
        gravitationalConstant: -40,
        centralGravity: .1,
        springLength: 20,
        springConstant: 0.1,
        damping: 0.9
    },
    maxVelocity: 4,
    solver: 'forceAtlas2Based',
    timestep: 0.35,
    stabilization: {iterations: 1},
  }
}

var network = new vis.Network(container, data, options);
network.on("select", function (params) {
    if(params.nodes.length > 0) {
        var sel_node_id = params.nodes[0];
        var sel_node = get_node_by_id(sel_node_id);
        console.log(desc[sel_node.data.name]);
        $("#tooltip").text("");
        $("#tooltip").text(desc[sel_node.data.name]);
        $('#mediabox').empty();
        if (imgs[sel_node.data.name])
            img_num = 0;
            img_max = imgs[sel_node.data.name].length;
            $('#mediabox').prepend('<img id="media" src="/static/img/articles/' 
                + sel_node.data.name + '/' + imgs[sel_node.data.name][0] + '" />');
            $('#mediabox').on('click', function() {
                img_num = img_num+1;
                $('#mediabox').empty();
                $('#mediabox').prepend('<img id="media" src="/static/img/articles/' 
                + sel_node.data.name + '/' + imgs[sel_node.data.name][img_num%img_max] + '" />');
                console.log(img_num);
                console.log(img_max);
            });
        $("#tooltip").css({visibility: "visible"});

    }
    else {
        $("#tooltip").css({visibility: "hidden"});
        $("#tooltip").text("");
        $('#mediabox').empty();
    }
});
network.setSize(width-250,height-50);
add_node({name: ida[start_node]});

$(document).ready(function() {
    $('#sidebar_form').submit(function(event) {
        event.preventDefault();
        if (!checkside())
        	return;
        var key = $('#navaddnode').val();
        if (!node_exists(key)) {
        	var ex_keys = JSON.stringify(get_existing_keys());
        	var ret_obj = {add_node: aid[key], ex_nodes: ex_keys}
        	$.post("/expand", ret_obj, function (return_data,status) {
                process_return_data(return_data);
			});
		}
    });
});

function process_edges(edges) {

    edges_convert(edges);
    var node1, node2;

    node1 = node_exists(edges[0]);
    for (var i = 2; i < edges.length; i +=2) {
        node2 = node_exists(edges[i]);
        if (!node2)
            node2 = add_node({name : edges[i]});
        add_edge(node1,node2,edges[i-1]);
        node1 = node2;
    }
}


function edges_convert(edges) {
    for (var i = 0; i < edges.length; i++) {
        if (ida[edges[i]])
            edges[i] = ida[edges[i]]
    }
}

function process_return_data(data) {
    data.edges = JSON.parse(data.edges)
    add_node({name : ida[data.add_node]});
    for (var i = 0; i < data.edges.length; i++) {
        process_edges(data.edges[i]);
    }
}

function node_exists(name) {
    for (var i = 0; i < nodesArray.length; i++) {
        if (nodesArray[i].label == name)
            return nodesArray[i];
    }
    return null;
}

function get_node_by_id(id) {
    for (var i = 0; i < nodesArray.length; i++) {
        if (nodesArray[i].id == id)
            return nodesArray[i];
    }
    return null;

}

function add_node(node_data) {
    id_counter += 1;
    if (aid[node_data.name]) {
            nodeObj = {id : id_counter,
                shape: 'circularImage',
                size: 10,
                font: {
                    size: 5,
                    face: 'Tahoma'
                },
                image: "/static/img/articles/" + node_data.name + "/profile.png",
                label : node_data.name,
                data : node_data}
    }
    else {
            nodeObj = {id : id_counter,
            shape: 'dot',
            size: 2,
            font: {
                size: 3,
                face: 'Tahoma'
            },
            label : node_data.name,
            data : node_data}
    }
    nodesArray.push(nodeObj)
    nodes.add(nodeObj);
    nodeIds.push(id_counter);
    return nodeObj;
}


function add_edge(node1, node2, label) {
    console.log(node1.label + " " + node2.label);
    edges.add({label: label.split("/").pop(), font: {align: 'middle', size: 3}, from: node1.id, to: node2.id, color:{color:'#c7c7c7', opacity:0.3}});

}



function get_existing_keys() {

	var ex_keys = [];
	for (var i = 0; i < nodesArray.length; i++) {
		if (aid[nodesArray[i].label])
		    ex_keys.push(aid[nodesArray[i].label]);
	}
	return ex_keys;
}

$('input.typeahead').typeahead({source: Object.keys(aid)});

function checkside() {
    var search_text = $('#navaddnode').val();
    if (!Object.keys(aid).includes(search_text)) {
        alert(search_text + " not in database.");
        return false;
    }
    return true;
}