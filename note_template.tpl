<!doctype HTML>
<html>

<head><title>view a note</title></head>

<body>

Welcome to the view a note page<p>
<form action="/newtag" method="get">
{{errors}}

<h2>view Note {{id}}</h2>

{{text}}<br>

created on: {{date_created}}

<h2>Tag</h2>
Comma separated. please dont put more than one for now<br>
<input type="text" name="tag" size="120" value="{{tag}}"><br>

<p>
<input type="submit" value="add a tag">

</body>
</html>
