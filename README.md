notesdb
=======
Database project for CMSI 486 Databases Independent Study

These files create a web app which acceses a MySQL database.

To interact with the web requests, python uses bottle. To interact with the database, python uses the driver MySQLdb.

The tables inside this relational database for now just include notes, tags, and a third table, note_tag, which allows a many to many relationship between the other two tables.

When I have more time, I will go in and make the database more realistic and useful.

For one, this means to allow the possibility of users that can add their own notes and view only their own, not others. Right now the database just stores notes and does not have a user login or notes specific to a certain person. Authentication is also something that will come hand in had with this.

I also plan to add more tables such as maps, calendar entries, and a phonebook/contact list which will enable notes to link to other usefull pieces of information.

The funcionality as of 12/10/13:
    can add notes by clicking the button on the home screen ('/')
    can view a specific note by entering it in the address ('/note/11', for example)
    
I will continue to add more features in
