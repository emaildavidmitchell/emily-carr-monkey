<!DOCTYPE html>
<html lang="en">

<html>
	<head>
		<meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1">
		<!-- Latest compiled and minified CSS -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		<link rel="stylesheet" type="text/css" href="static/css/header.css">
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-network.min.css">

		<!-- jQuery library -->
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

		<!-- Latest compiled JavaScript -->
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
		
    	<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-3-typeahead/4.0.1/bootstrap3-typeahead.min.js"></script>

    	<script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>


    	<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/svg.js/2.6.3/svg.min.js"></script>
    	<script src="static/js/svg.draggable.js"></script> -->

		<title>Linked Modernisms</title>
	</head>
	<body>


	<div class="container-fluid navbar-default"
		<nav class="navbar navbar-fixed-top">
			<div class="container-fluid">
				<div class="navbar-header">
					<a class="navbar-left" href="/"><img src="/static/img/LinkedModernismHEL.svg" height="40" width="110" class="d-inline-block align-top"></a>
				</div>
				<ul class="nav navbar-nav navbar-left">
					<li><a href="/examples">Examples</a></li>
					<li><a href="/about">About</a></li>
				</ul>
				<form class="navbar-form navbar-right form" action="/network" method="get" onSubmit="return checkhead()"
				autocomplete="off">
					<div class="form-group">
						<input type="text" class="form-control typeahead" id="navsearch" name="search" placeholder="Search">
					</div>
					<button type="submit" class="btn btn-default">Search</button>
				</form>
			</div>
		</nav>
	</div>
	
	<script>
		var aid = {{ aid|tojson }};
		var ida = {{ ida|tojson }};
		$('input.typeahead').typeahead({source: Object.keys(aid)});
		function checkhead() {
		    var search_text = $('#navsearch').val();
		    if (!Object.keys(aid).includes(search_text)) {
		        alert(search_text + " not in database.");
		        return false;
		    }
		}
	</script>
