<link rel="stylesheet" type="text/css" href="static/css/sidebar.css">
<div class="wrapper">
    <nav id="sidebar">
        <form class="form" id="sidebar_form" action="/expand" method="post" onSubmit="return checkside()">
            <div class="form-group row">
                <div class=" col-xs-offset-1 col-xs-10 ">
                    <input class="form-control input-sm typeahead" id="navaddnode" type="text" name="add"
                    placeholder="Add node" autocomplete="off">
                </div>
            </div>
        </form>
        <ul class="list-unstyled components">
        </ul>
    </nav>
</div>

