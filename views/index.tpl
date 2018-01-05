{% include "header.tpl" %}

	<div class="container">
		<div class="row">
		<form class="form" action="/network" method="get" onSubmit="return check()">
			<div class="form-group">
				<input class="form-control typeahead" placeholder="Search" name="search" id="search" autocomplete="off">
			</div>
			<button type="submit" class="btn btn-default">Submit</button>
	  	</form>
	  </div>
  </div>
	<script>
		var articles = {{ articles|tojson }};
		$('input.typeahead').typeahead({source: articles});
		function check() {
			var search_text = $('#search').val();
			if (!articles.includes(search_text)) {
				alert(search_text + " not in database.");
				return false;
			}
		}
	</script>
{% include "footer.tpl" %}
