<!doctype HTML>
<html>

<head><title>Create a new note</title></head>

<body>

Welcome        <a href="/">home</a> | <a href="/">Home</a><p>
<form action="/newnote" method="POST">
{{errors}}

<h2>note Entry<h2>
<textarea name="body" cols="120" rows="20">{{body}}</textarea><br>

<h2>Tag</h2>
Comma separated. please dont put more than one for now<br>
<input type="text" name="tag" size="120" value="{{tag}}"><br>

<p>
<input type="submit" value="Submit">

</body>
</html>

