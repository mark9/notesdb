import bottle
import MySQLdb
import cgi
import re

# This route is the main page of the database
# redirects to the notes main page
@bottle.route('/')
def app_index():
    bottle.redirect("/notesmain")

@bottle.get("/notes")
def main1():
    bottle.redirect("/notesmain")

@bottle.get("/notes/")
def main2():
    bottle.redirect("/notesmain")

# This route is the main page of the notes table
# fetches the first 5 rows 
@bottle.route('/notesmain')
def notes_index():
    results = sql_noparam("select * from notes order by _id desc limit 5")
    l = format_notes(results)
    return bottle.template("template_notes_main", dict(notes=l), errors="")

# This page fetches all the rows of the notes table
@bottle.route('/notesall')
def notes_all():
    results = sql_noparam("select * from notes order by _id desc")
    l = format_notes(results)
    return bottle.template("template_notes_all", dict(notes=l), errors="")

@bottle.get('/newnote')
def get_newnote():
    return bottle.template("template_notes_new", dict(body = "", errors="", tag=""))

@bottle.post('/newnote')
def post_newnote():
    text = bottle.request.forms.get("body")
    tags = bottle.request.forms.get("tags")
    #text = cgi.escape(text)
    #tags = cgi.escape(tags, quote=True)
    #tags = cgi.escape(tags)
    if text == "":
        errors = "note must contain text"
        return bottle.template("template_note_new", dict(body=text, tags=tags, errors=errors))
    else:
        # insert note
        cur=db.cursor()
        sql_param("insert into notes (text) values (%s)", text)
        results = sql_noparam("select last_insert_id()")
        # to get the id of this note, get last_insert_id()
        note_id = str(results[0][0])
        
        # insert tags
        array = array_tags(tags)
        #check each tag
        for tag in array:
            if tag != "":
                cur=db.cursor()
                cur.execute("select count(*) from tags where tag=%s", tag)
                results=cur.fetchall()
                # if the tag is not in the table already, do the following:
                if results[0][0] == 0:
                    cur.execute("insert into tags (tag) values (%s)", tag)
                # now that it is in there for sure, get the id
                db.commit()
                cur.execute("select _id from tags where tag=%s", tag)
                results=cur.fetchall()
                tag_id = str(results[0][0])
                # and make note_tag connection
                #cur.execute("insert into note_tag (_id_note, _id_tag) values (%s, %s)", note_id, tag_id)
                cur.executemany("insert into note_tag (_id_note, _id_tag) values (%s, %s)", [(note_id, tag_id),])
        
        db.commit()
        #sql = """select * from notes"""
        #cur.execute(sql)
        #results=cur.fetchall()
        #l = ''
        #for row in results:
        #    print row[1]
        
        # now bottle.redirect back to the main notes page
        bottle.redirect("/notesmain")

@bottle.get("/notes/note_not_found")
def note_not_found():
    return "Sorry, note not found"

# Displays a particular note
@bottle.get("/notes/<id>")
def show_note(id="notfound"):
    id = cgi.escape(id)
    results = sql_param("select count(*) from notes n where n._id=%s", id)
    
    # if note id doesn't exist, redirect
    if results[0][0] == 0:
        print results[0][0]
        bottle.redirect("/notes/note_not_found")
        
    else:
        # get note information
        results = sql_param("select * from notes n where n._id=%s", id)
        a = format_note(results)
        return bottle.template("template_notes_key", id=a[0], text=a[1], creation_date=a[2], tags=read_tags(a[0]), errors="")

@bottle.post('/newtag')
def add_newtag():
    tag = bottle.request.forms.get("tag")
    note_id = bottle.request.forms.get("id")
    
    # if values not good, redirect to view with errors
    if tag == "":
        # user did not fill in enough information
        bottle.redirect("/notes/<note_id>")
    else:
        
        # check if the tag has not already been created
        tag = cgi.escape(tag)
        cur.execute("select * from tags t where t.tag='%s'", tag)
        results=cur.fetchall()
        
        if row[0] == '':
            # if it doesn't exist, insert the tag for the first time
            cur.execute("insert into tags (tag) values ('%s');", tag)
            db.commit()
        
        # get the id of the tag
        cur.execute("select * from tags t where t.tag='%s'", tag)
        results=cur.fetchall()
        tag_id = row[0]
        print ('the tag inserted is' + row[0])
        
        # redirect back
        bottle.redirect("/notes/<note_id>")

@bottle.get('/tags/<tag>')
def show_notes_by_tag(tag="notfound"):
    tag = cgi.escape(tag)
    results = sql_param("select count(*) from tags t where t.tag=%s", tag)
    
    # if tag id doesn't exist, redirect
    if results[0][0] == 0:
        print results[0][0]
        bottle.redirect("/tag/tag_not_found")
        
    else:
        # get note information
        results = sql_param("select * from notes n join note_tag nt on nt._id_note=n._id join tags t on t._id=nt._id_tag where t.tag=%s", tag)
        l = format_notes(results)
        return bottle.template("template_tags_tag", dict(notes=l), title=tag, errors="")

# helper functions
def format_note(results):
    return ( results[0][0], results[0][1], fixup_date(results[0][2]))

def format_notes(results):
    l = []
    for row in results:
        num = row[0]
        date = fixup_date(row[2])
        tags=read_tags(num)
        l.append({'id':num, 'text':row[1], 'tags':tags, 'creation_date':date})
    return l

# used for the home page queries which just are looking for a list of notes to be returned
# could also be used for retreive notes by tag
def read_notes(sql):
    results = sql_noparam(sql)
    l = []
    for row in results:
        num = row[0]
        date = fixup_date(row[2])
        tags=read_tags(num)
        l.append({'id':num, 'text':row[1], 'tags':tags, 'creation_date':date})
    return l

# given id, perform join to get tags
def format_tags(results):
    l = []
    for row in results:
        l.append(row[0])
    return l
	
def read_tags(id):
    results = sql_param("select t.tag from tags t join note_tag nt on t._id=nt._id_tag where nt._id_note=%s", id)
    l = []
    for row in results:
        l.append(row[0])
    return l
	
# executes an sql query that doesnt need a parameter inputted
def sql_noparam(sql):
	cur.execute(sql)
	results = cur.fetchall()
	db.commit()
	return results

# executes an sql query that does need a parameter inputted
def sql_param(sql, param):
	cur.execute(sql, param)
	return cur.fetchall()

def fixup_date(date):
    formatted = date.strftime("%A, %B %d %Y at %I:%M%p") # fix up date
    return formatted

def array_tags(tags):
    whitespace = re.compile('\s')
    nowhite = whitespace.sub("",str(tags))
    tags_array = nowhite.split(',')
    new = []
    for tag in tags_array:
        if tag not in new and tag != "":
            new.append(tag)
    return new



db=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
#db=MySQLdb.connect(read_default_file='./config_file.mysql')
#db=MySQLdb.connect(read_default_file='~/my.cnf')
cur=db.cursor()

bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=8082)
