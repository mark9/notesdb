<!doctype HTML>
<html>

<head><title>Notes Database</title></head>

<body>

Welcome to the notes database<br>
This is the view a note page<p>
{{errors}}

To look at a different table: (click here for contacts, calendar, etc)<br>

<h2>view Note {{id}}</h2>


<a href="/notesmain">return to home</a><br>
search notes(doesnt work yet)<br>
<br>
Displaying the requested note.
view note:<br>
<a href="/notes/{{id-1}}">previous</a>      <a href="/notes/{{id+1}}">next</a>
<br><br><hr>

{{text}}<br>
<hr><br>

tags:
%for tag in tags:
<a href="/tags/{{tag}}">{{tag}}</a> 
%end
<br><br>
created {{creation_date}}
<br><br>
<a href="/notes/{{id}}">view note {{id}}</a><br>
edit note(doesnt work yet)
<p>

</body>
</html>
