<!doctype HTML>
<html>

<head><title>Notes Database: create a new note</title></head>

<body>

Welcome to the notes database       <a href="/">home</a> | <a href="/">Home</a><p>
This is the page to create a new note
<form action="/newnote" method="POST">
{{errors}}

<h2>Note<h2>
<textarea name="body" cols="120" rows="5">{{body}}</textarea><br>

<h2>Tags</h2>
Comma separated. please dont put more than one for now<br>
<input type="text" name="tag" size="120"><br>

<p>
<input type="submit" value="Submit">

</body>
</html>

