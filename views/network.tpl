{% include('header.tpl') %}
		
		<link rel="stylesheet" href="/static/css/network.css">
		<div class="container-fluid" id="graph-container">
			<svg width=100% height=100% id="graph" shape-rendering="geometricPrecision"></svg>
			<div id="infobar">
				<div id="tooltip"></div>
				<div id="mediabox"></div>
				<div class="btn-group" id="btns">
					<button type="button" class="btn btn-primary" id="desc" onclick="change_tooltip(this.id)">Descr.</button>
					<button type="button" class="btn btn-primary" id="attr" onclick="change_tooltip(this.id)">Links</button>
					<button type="button" class="btn btn-primary" id="type" onclick="change_tooltip(this.id)">Types</button>
				</div>
			</div>
		</div>
			
			<script src="https://d3js.org/d3.v4.min.js"></script>
			<script src="/static/javascript/network_script.js"></script>
			<script>
				/*var node_data = { label = "{{ node_data.label }}",


							
				};*/
				console.log(node_data);
				//var imgs = <%- JSON.stringify(imgs) %>;
				var node_set = [];
				var edge_set = [];
				add_node(node_set, edge_set, node_data, false, 0);
			</script>
			<script type="text/javascript" src="/static/javascript/d3Graph.js"></script>
	</body>
</html>

