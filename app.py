import bottle
import MySQLdb
import cgi
import re

# This route is the main page of the database
# redirects to the notes main page
@bottle.route('/')
def app_index():
    bottle.redirect("/notesmain")

# This route is the main page of the notes table
# fetches the first 5 rows 
@bottle.route('/notesmain')
def notes_index():
    #sql = """select count(*) from notes"""
    sql = """select * from notes order by _id desc limit 5"""
    cur.execute(sql)
    #db.commit()
    results=cur.fetchall()
    #l = ''
    l = []
    for row in results:
        num = row[0]
        date = fixup_date(row[2])
        l.append({'id':num, 'text':row[1], 'creation_date':date})
        #l=l+str(row[0])+' '+str(row[1])+' '+str(row[2])+' <br>'
    #return bottle.template("template_mainpage", notes=l, errors="", tag="")
    return bottle.template("template_notes_main", dict(notes=l), errors="", tag="")

# This page fetches all the rows of the notes table
@bottle.route('/notesall')
def notes_display():
    sql = """select * from notes order by _id desc"""
    cur.execute(sql)
    results=cur.fetchall()
    l = []
    for row in results:
        num = row[0]
        date = fixup_date(row[2])
        l.append({'id':num, 'text':row[1], 'creation_date':date})
    return bottle.template("template_notes_all", dict(notes=l), errors="", tag="")

def fixup_date(date):
    formatted = date.strftime("%A, %B %d %Y at %I:%M%p") # fix up date
    return formatted

def array_tags(tags):
    whitespace = re.compile('\s')
    nowhite = whitespace.sub("",str(tags))
    tags_array = nowhite.split(',')
    cleaned = []
    for tag in tags_array:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)
    return cleaned

@bottle.get('/newnote')
def get_newnote():
    return bottle.template("template_notes_new", dict(body = "", errors="", tag=""))

@bottle.post('/newnote')
def post_newnote():
    text = bottle.request.forms.get("body")
    print 'text inserted was: ' +text
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
        cur.execute("insert into notes (text) values (%s)", text)
        cur.execute("select last_insert_id()")
        # to get the id of this note, get last_insert_id()
        results=cur.fetchall()
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

@bottle.get("/notes")
def main1():
    bottle.redirect("/notesmain")

@bottle.get("/notes/")
def main2():
    bottle.redirect("/notesmain")

# Displays a particular note
@bottle.get("/notes/<id>")
def show_note(id="notfound"):
    id = cgi.escape(id)
    # check if note id exists
    cur.execute("select count(*) from notes n where n._id=%s", id)
    results=cur.fetchall()
    
    # if note id doesn't exist, redirect
    if results[0][0] == 0:
        print results[0][0]
        bottle.redirect("/notes/note_not_found")
        
    else:
        # get note information
        cur.execute("select * from notes n where n._id=%s", id)
        results=cur.fetchall()
        idno = results[0][0]
        note = results[0][1]
        date = fixup_date(results[0][2])
        
        # perform join to get related tags
        cur.execute("select t.tag from tags t join note_tag nt on t._id=nt._id_tag where nt._id_note=%s", id)
        results=cur.fetchall()
        
        l = []
        for row in results:
            print row[0]
            l.append(row[0])
        
        return bottle.template("template_notes_key", id=idno, text=note, date_created=date, tags=l, errors="")

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
        
        # to make the connection, insert into note_tag relationship table
        cur.execute("insert into note_tag (_id_note, _id_tag) values ('%s,%s');", note_id, tag_id)
        db.commit()
        
        # redirect back
        bottle.redirect("/notes/<note_id>")

#does not work yet
@bottle.get('/tags/<id>')
def show_notes_by_tag(id="notfound"):
    id = cgi.escape(id)
    # check if tag id exists
    cur.execute("select count(*) from tags t where t._id_tag=%s", id)
    results=cur.fetchall()
    
    # if tag id doesn't exist, redirect
    if results[0][0] == 0:
        print results[0][0]
        bottle.redirect("/tag/tag_not_found")
        
    else:
        # get note information
        cur.execute("select * from notes n where n._id=%s", id)
        results=cur.fetchall()
        idno = results[0][0]
        note = results[0][1]
        date = fixup_date(results[0][2])
        
        # perform join to get related tags
        cur.execute("select t.tag from tags t join note_tag nt on t._id=nt._id_tag where nt._id_note=%s", id)
        results=cur.fetchall()
        
        l = []
        for row in results:
            print row[0]
            l.append(row[0])
        
        return bottle.template("template_notes_key", id=idno, text=note, date_created=date, tags=l, errors="")

db=MySQLdb.connect(host=host,port=3306,user=user,passwd=passwd,db=db)
#db=MySQLdb.connect(read_default_file='./config_file.mysql')
#db=MySQLdb.connect(read_default_file='~/my.cnf')
cur=db.cursor()

bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=8082)
