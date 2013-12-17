<!doctype HTML>
<html>

<head><title>Notes Database</title></head>

<body>

Welcome to the notes database<br>
This is the main page<p>
{{errors}}

To look at a different table: (click here for contacts, calendar, etc)<br>

<h2>List of Notes</h2>
Displaying the 5 most recent notes.

<a href="/notesall">view all</a><br>
search notes<br>
<br>
<form action="/newnote" method="get">
<input type="submit" value="add a new note">

<hr>

%for note in notes:
{{!note['text']}}<br><br>
tags:
%for tag in note['tags']:
<a href="/tags/{{tag}}">{{tag}}</a> 
%end
<br>
created {{note['creation_date']}}
<br>
<a href="/notes/{{note['id']}}">edit note {{note['id']}}</a><br>
<hr>
%end

<p>

</body>
</html>
