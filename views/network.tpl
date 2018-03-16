{% include('header.tpl') %}
<link rel="stylesheet" href="/static/css/network.css">
<div class="row">
	<div class="col-xs-2">
		{% include('sidebar.tpl') %}
	</div>
	<div class="col-xs-8" id ="dm">
		<div class="container-fluid" id="graph-container">
			<script>
				var start_node = {{ s_node|tojson }}
				var desc = {{desc|tojson}}
				var imgs = {{imgs|tojson}}
			</script>
		</div>
	</div>
	<div class="col-xs-2">
		{% include('infobar.tpl') %}
	</div>
</div>
<script src="static/js/graph.js"></script>

