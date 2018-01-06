
/* 
	svg is the scalable vector graphic division which graphics are appended to
	r is the default radius of the nodes
	iw and ih are the image width and height of the nodes
	transform allows the svg division to be zoomed in on
	e represents the group of edges on the svg
	g represents the nodes and text on the svg
*/

var svg = d3.select("#graph"),
	w = parseInt(svg.style("width")),
	h = parseInt(svg.style("height")),
	r = 10,
	transform = d3.zoomIdentity,
	e = svg.append("g"),
	activeNode = undefined,
	activeData = undefined,
	imagePos = 0,
	g = svg.append("g");

/*
	moves the current selection to the front of the svg
*/

d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

/*
	scaleExtent determines how far svg will zoom	
*/

svg.call(d3.zoom()
    .scaleExtent([1 / 2, 8])
    .on("zoom", zoomed));

svg.on("dblclick.zoom", null);

$('#mediabox').on("click",next_image);


update();

/*
	update uses the d3 update pattern to link html elements with data
	group node elements containing circles and text are linked to each element of the node set
	lines are linked to each element of the edge set
*/


function update() {
	var node_update = g.selectAll("g")
			.data(node_set, function (d) {
				return d.id;
			});

		var enter = node_update.enter()
			.append("g")
			.attr("class","nodes")
			.attr("",init_position)
			.attr("x", function(d) {
				return d.x;
			})
			.attr("y", function(d) {
				return d.y;
			})
			.attr("id", function(d) {
				return d.id;
			})
			.call(d3.drag()
				.on("start", dragstarted)
				.on("drag", dragged)
				.on("end", dragended))
			.on("click",clickon);

		enter.append("circle")
			.attr("cx", function(d,i) {
				return d.x;
			})
			.attr("cy", function(d,i) {
				return d.y;
			})
			.attr("r", function(d,i) {
				return d.r+2;
			})
			.attr("fill","black");


		enter.append("svg:image")
			.attr("xlink:href",  function(d) { 
				return "img/articles/" + d.name + "/profile.png";
			})
			.attr("x", function(d,i) {
				return d.x-d.r;
			})
			.attr("y", function(d,i) {
				return d.y-d.r;
			})
			.attr("height", function(d,i) {
				return 2*d.r;
			})
			.attr("width", function(d,i) {
				return 2*d.r;
			})

		enter.append("text")
			.attr("class","name")
			.attr("x", function(d,i) {
				return d.x;
			})
			.attr("y", function(d,i) {
				return d.y;
			})
			.attr("text-anchor","middle")
			.text(function(d) {
				return text_sample(d);
			})
			.style("font-size", function(d) {
				return get_font_size(d);
			})
			.style("font-family", "sans-serif")
			.style("font-weight","bold");

    	enter.append("text")
			.attr("class","button")
			.attr("x", function(d,i) {
				return d.x;
			})
			.attr("y", function(d,i) {
				return d.y-d.r-5;
			})
			.attr("text-anchor","middle")
			.text("+")
			.style("font-size", 25)

		node_update.merge(enter);

		var edge_update = e.selectAll("g")
			.data(edge_set, function (d) {
				return d.source + "-" + d.dest; 
			});

		var enter = edge_update.enter()
			.append("g")
			.attr("class","edges")
			.append("line")
			.attr("x1", function(d) {
				return d.source.x;
			})
			.attr("y1", function(d) {
				return d.source.y;
			})
			.attr("x2", function(d) {
				return d.dest.x;
			})
			.attr("y2", function(d) {
				return d.dest.y;
			})
            .attr("stroke", "#999")
            .attr("stroke-width", "2")
            .attr("stroke-opacity", 0.3)
            .on("mouseover", edgemouseover)
            .on("mouseout", edgemouseout)
			.append("title")
			.text(function (d) {
				return d.relation;
			});

		edge_update.merge(enter);
		update_visibility();
}


/*
	action when node double clicked on
	nodes are expanded to create links to other nodes
	if children are visible make them invisible else visible
	update svg to reflect changes
*/

function clickon(d) {

	if (d3.event.srcElement.classList.contains("button")) {
		expand(d);
		return;
	}

    clickedNode = d3.select(this);

    if (clickedNode.classed("selected")) {
    	dehighlight(clickedNode);
    	clickedNode.classed("selected", false);
    	activeNode = undefined;
    } else if (!activeNode) {
        highlight(clickedNode,d);
    	clickedNode.classed("selected", true);
    	activeNode = clickedNode;
    	activeData = d;
	} else {
        dehighlight(activeNode);
    	activeNode.classed("selected", false);
    	activeNode = clickedNode;
    	activeData = d;
    	highlight(clickedNode, d);
    	clickedNode.classed("selected", true);
	}

}

function expand(d) {

    if (!d.expanded) {
        expand_node(node_set, edge_set, d.id, update);
    }
    else {
        d.extended = !d.extended;
        d.children.forEach( function (n) {
            if (n.visibility === "hidden")
                n.visibility = "visible";
            else
            if (n.children.length === 0)
                n.visibility = "hidden";
        });
        update_visibility();
    }

}

function zoomed() {
  g.attr("transform", d3.event.transform);
  e.attr("transform", d3.event.transform);
}

function dragstarted(d) {
  d3.select(this).raise().classed("active", true);

}

function dragged(d) {

  d3.select(this).attr("x", d.x = d3.event.x).attr("y", d.y = d3.event.y);
  d3.select(this).selectAll("circle").attr("cx",d.x).attr("cy", d.y);
  d3.select(this).selectAll("image").attr("x",d.x-d.r).attr("y", d.y-d.r);
  d3.select(this).selectAll(".name").attr("x", d.x).attr("y", d.y);
  d3.select(this).selectAll(".button").attr("x", d.x).attr("y", d.y-d.r-5);

    d3.select(this).attr("", function(d) {
  	if (d.extended)
  		drag_children(d,d3.event);
  });

  e.selectAll(".edges")
  	.select("line")
  	.attr("x1", function(d) {
  		return d.source.x;
  	})
  	.attr("y1", function(d) {
  		return d.source.y;

  	})
  	.attr("x2", function(d) {
  		return d.dest.x;
  	})
	.attr("y2", function(d) {
  		return d.dest.y;
  	});

}

function dragended(d) {
  d3.select(this).classed("active", false);
}

function highlight(clickedNode,d) {


    clickedNode.moveToFront();

    clickedNode.selectAll("circle")
        .attr("r", function (d) {
            d.r = (r*8);
            return d.r+2;
        });

    clickedNode.selectAll("image")
        .attr("height", function (d) {
            return 2*d.r;
        })
        .attr("width", function (d) {
            return 2*d.r;
        })
        .attr("x", function (d) {
            return d.x-d.r;
        })
        .attr("y", function (d) {
            return d.y-d.r;
        })

    clickedNode.selectAll(".name")
        .text(function (d) {
            return d.name;
        })
        .style("font-size", function(d) {
            return get_font_size(d,3);
        });

    clickedNode.selectAll(".button")
		.attr("y", function (d) {
			return (d.y-d.r-5);
		});

    show_bars();


    $("#tooltip").text(d.desc);

    link = "https://www.rem.routledge.com/search?searchString=" + d.name + "&newSearch=";

    $("#tooltip").append('<a href='+link+'>' + "Search on REM" + '</a>');

    $('#mediabox').empty();
	if (imgs[d.name].length > 0) {
        $('#mediabox').prepend('<img id="media" src="/img/articles/' + d.name + '/' + imgs[d.name][0] + '" />');
        imagePos = 0;
    }

}


function dehighlight(clickedNode) {

    clickedNode.selectAll("circle")
        .attr("r", function (d) {
            d.r = r;
            return d.r+2;
        });

    clickedNode.selectAll("image")
        .attr("height", function (d) {
            return 2*d.r;
        })
        .attr("width", function (d) {
            return 2*d.r;
        })
        .attr("x", function (d) {
            return d.x-d.r;
        })
        .attr("y", function (d) {
            return d.y-d.r;
        })

    clickedNode.selectAll(".name")
        .text(function(d) {
            return text_sample(d);
        })
        .style("font-size", function(d) {
            return get_font_size(d);
        });

    clickedNode.selectAll(".button")
        .attr("y", function (d) {
            return (d.y-d.r-5);
        });

    hide_bars();

}

function hide_bars() {
    $("#tooltip").css({visibility: "hidden"});

    $("#btns").css({visibility: "hidden"})

    $("#mediabox").css({visibility: "hidden"});
}


function show_bars() {
    $("#tooltip").css({visibility: "visible"});

    $("#btns").css({visibility: "visible"})

    $("#mediabox").css({visibility: "visible"});
}

function edgemouseover(d) {

	d3.select(this)
        .attr("stroke", "black")
        .attr("stroke-width", "5")

}

function edgemouseout(d) {

    d3.select(this)
        .attr("stroke", "#999")
        .attr("stroke-width", "2")

}

function text_sample(d) {
	if (d.name.length > 20)
		return d.name.slice(0,20) + "...";
	else
		return d.name;
}

function get_font_size(d, mult=1) {
	return mult*10 + "px";
}

function pos_around(min_dist,max_dist) {

	var rad = Math.random()*(max_dist-min_dist) + min_dist;
	var ang = Math.random()*2*Math.PI;
	var y = rad*Math.sin(ang);
	var x = rad*Math.cos(ang);
	return [x,y];
}

function init_position(d,i) {
	d.r = r;
	
	if (d.id == 0) {
		d.x = w/2;
		d.y = h/2;
	}
	else {
		
		var min = 100;
		var max = 110;
		do {
			var pos = pos_around(min,max);
			pos[0] = pos[0]+d.parent.x;
			pos[1] = pos[1]+d.parent.y;
			max = max+2;
		} while(is_occ(pos,50));
		d.x = pos[0];
		d.y = pos[1];
	}
}

function is_occ(pos,r) {

	var node;
	for (var i = 0; i < node_set.length; i++) {
		node = node_set[i];
		if (node.visibility == "visible") {
			var dist = (Math.pow(pos[0]-node.x,2)+Math.pow(pos[1]-node.y,2));
			if (dist < Math.pow(r,2))
				return true;
		}
		
	}
	return false;
}

function update_visibility() {

	g.selectAll("g")
		.style("visibility", function (d) {
			return d.visibility;
		});


	e.selectAll("g")
		.style("visibility", function (d) {
			if ((d.source.visibility === "hidden") || (d.dest.visibility === "hidden"))
				return "hidden";
			else
				return "visible";
		});
}

/*

	When parent is dragged, drag children to new position as well

 */

function drag_children(d,event) {
	d.children.forEach( function(node) {
		if (node.expanded === false) {
			node.x += event.dx;
			node.y += event.dy;
		}
	});
	update_position();

}

/*
	Iterate through all the elements and move them to correct position
 */

function update_position() {
	g.selectAll(".nodes").attr("x", function (d) {return d.x;}).attr("y", function (d) {return d.y;});
	g.selectAll("circle").attr("cx", function (d) {return d.x;}).attr("cy", function (d) {return d.y;});
	g.selectAll("image").attr("x", function (d) {return d.x-d.r;}).attr("y", function (d) {return d.y-d.r;});
	g.selectAll(".name").attr("x", function (d) {return d.x;}).attr("y", function (d) {return d.y;});
	g.selectAll(".button").attr("x", function (d) { return d.x }).attr("y", function (d) { return d.y - d.r -5});
	e.selectAll(".edges").select("line")
		.attr("x1", function(d) {return d.source.x; })
		.attr("y1", function(d) {return d.source.y;})
		.attr("x2", function(d) {return d.dest.x;})
		.attr("y2", function(d) {return d.dest.y;});
}

/*
	Change the contents of the tooltip
 */

function change_tooltip(id) {

	var text = "";
	switch(id) {
		case "desc":
			text = activeData.desc;
			break;
		case "attr":
			text = activeData.links.reduce((function(acc, obj) { return acc + "\n" + obj.l.value}), "");
			console.log(activeData.links);
			break;
		case "type":
			text = activeData.type.reduce((function(acc, obj) { return acc + "\n" + obj.t.value }),"");
			break;
	}

    $("#tooltip").text(text);

}

function next_image() {

    $('#mediabox').empty();
    if (imgs[activeData.name].length > 0) {
        imagePos = (imagePos+1)%imgs[activeData.name].length;
        $('#mediabox').prepend('<img id="media" src="/img/articles/' + activeData.name + '/' + imgs[activeData.name][imagePos] + '" />');
    }
}
