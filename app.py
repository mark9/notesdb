import bottle
import MySQLdb
import cgi

@bottle.route('/')
def app_index():
    #sql = """select count(*) from notes"""
    sql = """select * from notes"""
    cur.execute(sql)
    #db.commit()
    results=cur.fetchall()
    l = ''
    #l = []
    for row in results:
        #row[2] = row[2].strftime("%A, %B %d %Y at %I:%M%p") # fix up date
        #l.append({'number':row[0], 'text':row[1], 'creation_date':row['date'],
        l=l+str(row[0])+' '+str(row[1])+' '+str(row[2])+' '
        #l=l+'\n'
    return bottle.template("mainpage_template", body=l, errors="", tag="")
    #return bottle.template("mainpage_template", dict(body=l), errors="", tag="")

@bottle.get('/newnote')
def get_newnote():
    return bottle.template("newnote_template", dict(body = "", errors="", tag=""))

@bottle.post('/newnote')
def post_newnote():
    text = bottle.request.forms.get("body")
    tag = bottle.request.forms.get("tag")
    if text == "":
        errors = "note must contain text"
        return bottle.template("newnote_template", dict(body=cgi.escape(text, quote=True), tag=tag, errors=errors))
    #insert it
    cur=db.cursor()
    cur.execute("insert into notes (text) values (%s)", text)
    cur.execute("insert into tags (tag) values (%s)", tag)
    db.commit()
    sql = """select * from notes"""
    cur.execute(sql)
    #results=cur.fetchall()
    #l = ''
    #for row in results:
    #    print row[1]

    # now bottle.redirect to the blog permalink
    bottle.redirect("/")


# Displays a particular note
@bottle.get("/note/<id>")
def show_note(id="notfound"):
    # check if note id exists
    cur.execute("select count(*) from notes n where n._id=%s", id)
    results=cur.fetchall()
    
    # if note id doesn't exist, redirect
    if results[0][0] == 0:
        bottle.redirect("/note_not_found")
        
    else:
        id = cgi.escape(id)
        cur.execute("select * from notes n where n._id=%s", id)
        results=cur.fetchall()
        id = results[0][0]
        text = results[0][1]
        date_created = results[0][2]
        return bottle.template("note_template", id=id, text=text, date_created=date_created, errors="", tag="")

@bottle.post('/newtag')
def add_newtag():
    tag = bottle.request.forms.get("tag")
    note_id = bottle.request.forms.get("id")
    
    # if values not good, redirect to view with errors
    if tag == "":
        # user did not fill in enough information
        bottle.redirect("/note/<note_id>")
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
        
        # to make the connection insert into note_tag relationship table
        cur.execute("insert into note_tag (_id_note, _id_tag) values ('%s,%s');", note_id, tag_id)
        db.commit()
        
        # redirect back
        bottle.redirect("/note/<id>")


db=MySQLdb.connect(host="mysql4.cs.lmu.edu",port=3306,user="mlawranc",passwd="keck",db="mlawranc")
cur=db.cursor()

bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=8082)
