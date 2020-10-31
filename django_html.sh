cat << _EOF_
<!DOCTYPE html>

{% load static %}

<html>
<head>
    <title></title>
    <link rel='stylesheet' href='{% static "sitepackages/bootstrap.min.css" %}'>

    <!-- <link rel='stylesheet' href='{% static "css/projectcss.css" %}'> -->
    
    <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
</head>

<body>

	<script src='{% static "sitepackages/jquery.min.js" %}'></script>
	<script src='{% static "sitepackages/popper.min.js" %}'></script>
    <script src='{% static "sitepackages/bootstrap.min.js" %}'></script>

    <!-- <script src='{% static "js/projectjs.js" %}'></script> -->
</body>

</html>
_EOF_