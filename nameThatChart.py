import binascii
import datetime
import json
import os
import time
from random import randint
import base64
import boto3
import wget
from PIL import Image
from flask import Flask, request, session, render_template, Response, jsonify
from flask import redirect
from flask_caching import Cache
from flask_compress import Compress
from flaskext.mysql import MySQL
import sys
from datetime import timedelta
from datasetManager import imagePrep as pics

#     <------------------Server configuration ------------------>
application = Flask(__name__)
mysql = MySQL()

# hash key
application.secret_key = binascii.hexlify(os.urandom(24))

# GZIP
COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500

# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_DATABASE_USER']
application.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_DATABASE_PASSWORD']
application.config['MYSQL_DATABASE_DB'] = os.environ['MYSQL_DATABASE_DB']
application.config['MYSQL_DATABASE_HOST'] = os.environ['MYSQL_DATABASE_HOST']

cache = Cache(config={'CACHE_TYPE': 'simple'})

# init
mysql.init_app(application)
cache.init_app(application)
Compress(application)


@app.before_request
def make_session_permanent():
    session.permanent = False
    app.permanent_session_lifetime = timedelta(minutes=10)
    if session.get("haha") is None:
        session["haha"] = False


# <------------------ Temp ------------------>


@ application.route('/putiton')
def putiton():
    if str(session.get("haha")) == 'True':
        session["haha"] = False
    else:
        session["haha"] = True
    return 'ok'


@ application.route('/navbar')
def navbar():
    return render_template("navbar.html")


@ application.route('/image2json')
def image2json():
    con = mysql.connect()
    cursor = con.cursor()
    ids = []
    cursor.execute(
        "SELECT DISTINCT imagepath,image.idimage,label FROM image INNER  JOIN textvote ON image.idimage= textvote.idimage INNER JOIN type  ON type.idtype= textvote.idtype")
    data = cursor.fetchall()

    result = '['

    for row in data:

        if row[1] not in ids:
            result += '{"path": "' + str(row[0]) + '","id":' + str(row[1]) + ',"Type":"' + str(row[2]) + '"},'
            ids.append(row[1])

    cursor.execute(
        "SELECT DISTINCT idimage,imagepath FROM image WHERE idimage NOT IN (SELECT DISTINCT (idimage) FROM textvote)")

    data = cursor.fetchall()
    for row in data:
        result += '{"path": "' + str(row[1]) + '","id":' + str(row[0]) + '},'

    result = result[:-1]
    result += ']'
    print(result)

    cursor.close()
    con.close()

    return result


#     <------------------ Classic render template ------------------>

@ application.route('/')
def hello_world():
    return render_template('index.html')


# View Qcm
@ application.route('/multiple')
def multiple():
    return render_template('multiple.html')


# View Textual D3js
@ application.route('/textual')
def textual():
    return render_template('textualimg.html')


# View of Swipes
@ application.route('/swipes')
def swipes():
    return render_template('swipes.html')


# View of textual with images
@ application.route('/textualimg')
def textualimg():
    session['haha'] = True
    return render_template('textualimg.html')


# View of admin tools
@ application.route('/admin')
def admin():
    return render_template('admin.html')


# Display user id from IP
@ application.route('/whatismyid')
def whatismyid():
    return str(getid(request.environ["REMOTE_ADDR"]))


# View to upload images into database
@ application.route('/uploadimg')
def uploadimg():
    return render_template('uploadimg.html')


@ application.route('/reverse')
def reverse():
    return render_template('reverse.html')


# View of images selection UI
@ application.route('/selectimg')
def selectimg():
    return render_template('selectimg.html')


# View of database of image display / selection
@ application.route('/display_image')
def display_image():
    return render_template('display_image.html')


@ application.route('/display_image/<id>')
def display_imageid(id):
    return render_template('display_image.html', test=id)


#     <------------------ Complex render template ------------------>

# Get started quizz
@ application.route('/quizz')
def quizz():
    temp = ['swipes', 'textualimg', 'multiple', 'selectimg']

    if session.get("page") is None:
        session['page'] = 0
        session['note'] = 0
        session['id'] = getid(request.environ["REMOTE_ADDR"])
    else:
        session['page'] += 1
    nb = session.get("page")
    if nb >= len(temp):
        session['page'] = 0
        session['note'] = 0
        session['id'] = getid(request.environ["REMOTE_ADDR"])
        nb = 0
    print(session['note'])
    return render_template(temp[nb] + ".html")


# main view with Random selection
@ application.route('/raw')
def mainraw():
    a = randint(0, 500)
    if a < 100:
        return render_template('textualimg.html')
    elif a < 200:
        return render_template('selectimg.html')
    elif a < 300:
        return render_template('swipes.html')
    elif a < 330:
        return render_template("multiple.html")
    else:
        return render_template("reverse.html")


# main view with taskforce motivation handling
@ application.route('/main')
def main():
    if session.get("lvl") is None:
        lvl = getlvl(request.environ["REMOTE_ADDR"])
    if session.get("lvl") is None:
        return redirect("/raw")
    else:
        lvl = session.get("lvl")
    print(str(session.get("task")) + " MOTIVATION")
    if int(session.get("task")) > 80 and int(session.get("lvl")) > 0:
        session['task'] = str(int(session.get("task")) + getcost(0, int(session.get("lvl"))))
        return render_template('textualimg.html')
    elif int(session.get("task")) > 50 and int(session.get("lvl")) > 0:
        session['task'] = str(int(session.get("task")) + getcost(1, int(session.get("lvl"))))
        rand = randint(0, 300)
        if rand < 130:
            return render_template('selectimg.html')
        elif rand < 290:
            return render_template('reverse.html')
        else:
            return render_template('multiple.html')
    elif int(session.get("task")) > 70 and int(session.get("lvl")) == 0:
        return render_template('textualimg.html')
    elif int(session.get("task")) > 40 and int(session.get("lvl")) == 0:
        session['task'] = str(int(session.get("task")) + getcost(1, int(session.get("lvl"))))
        rand = randint(0, 300)
        if rand < 130:
            return render_template('selectimg.html')
        elif rand < 290:
            return render_template('reverse.html')
        else:
            return render_template('multiple.html')
    else:
        session['task'] = str(int(session.get("task")) + getcost(2, int(session.get("lvl"))))
        return render_template('swipes.html')


@ application.route('/generated/<hash>')
def gen(hash):
    hash = base64.b64decode(hash).decode("utf-8")
    print(hash + " Hash")
    vals = str(hash).split("/")
    print(str(vals) + " Vals")
    return render_template(str(vals[0]) + ".html", test=vals[1])


#     <------------------ Task saving ------------------>

# Quizz note saving
@ application.route('/savenote', methods=['POST'])
def savenote():
    session['note'] = int(request.form["note"]) + int(session.get("note"))
    if (session['page'] == 3):

        note = session['note']
        lvl = 0
        if note > 11:
            lvl = 2
        elif note > 5:
            lvl = 1
        con = mysql.connect()
        cursor = con.cursor()

        cursor.execute(
            " UPDATE  `user` SET lvl ='" + str(lvl) + "', taskforce ='0' WHERE iduser =" + str(session.get('id')))
        cursor.close()

        session["lvl"] = str(lvl)
        session["task"] = str(int(50 * lvl))
        con.commit()
        con.close()

    return 'ok'


# Mapping to save multiple (QCM) task
@ application.route('/savemultiple', methods=['POST'])
def savemultiple():
    idimage = request.form.get("idimage")
    idtype = request.form.get("idtype")
    url = request.form.get("url")
    idu = getid(request.environ['REMOTE_ADDR'])
    now, timestamp = gettimes()
    con = mysql.connect()
    cursor = con.cursor()
    final = "INSERT INTO multiple (idimage,idtype,iduser,`time`,`date`,`event`,url) VALUES (" + str(
        idimage) + "," + str(
        idtype) + "," + str(idu) + ",'" + str(timestamp) + "','" + str(now) + "','chosen','" + url + "') "

    cursor.execute(final)
    cursor.close()
    con.commit()
    con.close()
    checkandup(idtype, idimage, 12)
    return 'ok'


# Mapping to save Textual task
@ application.route('/savetext', methods=['POST'])
def savetext():
    name = request.form["name"]
    name = name.replace("'", "\\'")
    now, timestamp = gettimes()

    con = mysql.connect()
    cursor = con.cursor()

    url = request.form.get("url")
    idim = request.form["id"]
    idu = getid(request.environ['REMOTE_ADDR'])
    idt = gettype(name)[0]

    query = "INSERT INTO textvote (iduser,time,date,event,idtype,idimage,url) VALUES(" + str(idu) + ",'" + str(
        timestamp) + "','" + str(now) + "','" + "submitted" + "'," + str(idt) + "," + str(idim) + ",'" + url + "')"

    cursor.execute(query)
    con.commit()

    cursor.close()
    con.close()

    checkandup(idt, idim, 40)

    return 'ok'


def checkandup(idtype, idimage, pts):
    con = mysql.connect()
    cursor = con.cursor()

    query = "SELECT * FROM result WHERE idtype=" + str(idtype) + " AND idimage=" + str(idimage)
    cursor.execute(query)
    data = cursor.fetchone()

    if data is None:
        query = "INSERT INTO result (idtype,idimage,score) VALUES (" + str(idtype) + "," + str(idimage) + "," + str(
            pts) + ")"
    else:
        query = "UPDATE result SET score = score+" + str(pts) + " WHERE idtype=" + str(idtype) + " AND idimage=" + str(
            idimage)

    cursor.execute(query)

    cursor.close()
    con.commit()
    con.close()


@ application.route("/saverev", methods=['post'])
def saverev():
    idu = getid(request.environ['REMOTE_ADDR'])
    idtype = request.form["idtype"]
    image = request.form.get('image')
    url = request.form.get("url")
    action = 'chosen'
    now, timestamp = gettimes()

    q = "INSERT INTO `reverse` (iduser,idimage,idtype,`time`,`date`,`event`,url) VALUES(" + str(idu) + "," + str(
        image) + "," + str(idtype) + ",'" + str(timestamp) + "','" + str(now) + "','" + action + "','" + url + "')"
    print(q)
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(q)

    cursor.close()
    con.commit()
    con.close()
    checkandup(idtype, image, 10)
    return 'ok'


# Save user choice into selection
@ application.route('/saveselect', methods=['POST'])
def saveselect():
    iduser = getid(request.environ['REMOTE_ADDR'])
    idtype = request.form['idtype']
    idimg = request.form['idimage']
    url = request.form.get("url")

    now, timestamp = gettimes()
    con = mysql.connect()
    cursor = con.cursor()
    q = "INSERT INTO selection (idimage,idtype,iduser,`time`,`date`,`event`,url) VALUES (" + str(idimg) + "," + str(
        idtype) + "," + str(
        iduser) + ",'" + str(timestamp) + "','" + str(now) + "','chosen','" + url + "')"
    print(q)
    cursor.execute(q)

    cursor.close()
    con.commit()
    con.close()
    checkandup(idtype, idimg, 20)
    return 'ok'


# Save one swipe on swipes
@ application.route('/saveswipe', methods=['POST'])
def saveswipe():
    idimage = request.form["idimage"]
    vote = request.form["vote"]
    idtype = request.form["idtype"]
    url = request.form.get("url")
    iduser = getid(request.environ['REMOTE_ADDR'])
    now, timestamp = gettimes()

    con = mysql.connect()
    cursor = con.cursor()

    q = "INSERT INTO swipe (idimage,idtype,iduser,vote,`time`,`date`,`event`,url) VALUES (" + str(idimage) + "," + str(
        idtype) + "," + str(
        iduser) + "," + str(to_bool(vote)) + ",'" + timestamp + "','" + now + "','swipe','" + url + "')"
    print(q)
    cursor.execute(q)

    cursor.close()
    con.commit()
    con.close()
    if str(vote) == 'true':
        checkandup(idtype, idimage, 5)
    else:
        checkandup(idtype, idimage, -15)
    return 'ok'


#     <------------------ Reports saving ------------------>

@ application.route("/report/<where>", methods=['POST'])
def reportgene(where):
    usrid = getid(request.environ['REMOTE_ADDR'])
    idimgs = str(request.form.get('ids')).split(",")
    url = request.form.get('url')
    print(idimgs)
    con = mysql.connect()
    cursor = con.cursor()

    for idimg in idimgs:
        q = "INSERT INTO report (idimage,iduser,label,`where`,url) VALUES (" + str(idimg) + "," + str(
            usrid) + ",'not a data graphics','" + where + "','" + url + "')"
        print(q)
        cursor.execute(q)

    con.commit()
    con.close()
    return 'ok'


#     <------------------ Tasks get ------------------>



# Mapping to get image to display in Textualimg
@ application.route('/getnextimg')
def getnextimg():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(
        "SELECT imagepath,idimage FROM image WHERE idimage NOT IN (SELECT DISTINCT (idimage) FROM textvote)  ORDER BY rand() LIMIT 1")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(
            "SELECT DISTINCT imagepath, image.idimage FROM textvote INNER JOIN image ON image.idimage=textvote.idimage GROUP BY idimage ORDER BY count(*) LIMIT 1")
        data = cursor.fetchone()
    cursor.close()
    con.close()
    return json.dumps(data)


@ application.route('/getimgmul')
def getimgmul():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "SELECT DISTINCT image.idimage,imagepath FROM result,image WHERE image.idimage= result.idimage AND image.idimage IN (SELECT idimage FROM result GROUP BY image.idimage HAVING count(idtype) > 3) ORDER BY rand() LIMIT 1")
    img = cursor.fetchone()
    cursor.execute(
        "SELECT DISTINCT label,type.idtype FROM type INNER JOIN result ON type.idtype=result.idtype WHERE idimage=" + str(
            img[0]) + " ORDER BY rand() LIMIT 4")

    data = cursor.fetchall()
    print(data)
    cursor.close()
    con.close()
    arr = ""
    for row in data:
        print(row)
        arr += '{"label":"' + str(row[0]) + '","idtype":"' + str(row[1]) + '"},'
    arr = arr[:-1]

    result = '{"image":{"id":"' + str(img[0]) + '","path":"' + img[1] + '"},' \
                                                                        '"types":[' + arr + ']}'
    return result


# Get set of images to display in selection
@ application.route('/getselect')
def getselect():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "SELECT type.idtype,label FROM result INNER JOIN type ON type.idtype = result.idtype WHERE type.idtype IS NOT NULL GROUP BY type.idtype,label HAVING count(idimage) > 5 ORDER BY rand() LIMIT 1")
    idtype = cursor.fetchone()

    cursor.execute(
        "SELECT DISTINCT imagepath,image.idimage FROM result INNER JOIN image ON image.idimage = result.idimage WHERE result.idtype = " + str(
            idtype[0]) + " ORDER BY rand() LIMIT 6")

    imgs = cursor.fetchall()
    cursor.close()
    con.close()
    result = '{' \
             '"name":"' + idtype[1] + '", ' \
                                      '"idtype":"' + str(idtype[0]) + '", ' \
                                                                      '"imgs": ['

    for row in imgs:
        result += '{"path": "' + str(row[0]) + '","idimage":' + str(row[1]) + '},'

    result = result[:-1]
    result += ']' \
              '}'
    print(result)

    return result


# Get set of 5 images & types to fill swipes
@ application.route('/getfive', )
def getfive():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "SELECT  DISTINCT image.idimage,imagepath,label,type.idtype FROM result INNER JOIN image ON image.idimage=result.idimage INNER JOIN type ON type.idtype= result.idtype  WHERE score > 20 ORDER BY rand() LIMIT 5")
    data = cursor.fetchall()

    result = "[ "

    for row in data:
        result += '{"path" : "' + str(row[1]) + '","label" : "' + row[2] + '","idimage":' + str(
            row[0]) + ',"idtype": ' + str(row[3]) + '},'
    result = result[:-1]
    result += " ]"
    cursor.close()
    con.close()
    print(result)
    return result


@ application.route('/getreverse')
def getreverse():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "SELECT type.idtype,label FROM result INNER JOIN type ON type.idtype = result.idtype WHERE type.idtype IS NOT NULL GROUP BY type.idtype,label HAVING count(idimage) > 3 ORDER BY rand() LIMIT 1")
    idt = cursor.fetchone()

    cursor.execute(
        "SELECT DISTINCT image.idimage,imagepath FROM result INNER JOIN image ON image.idimage = result.idimage WHERE result.idtype = " + str(
            idt[0]) + " ORDER BY rand() LIMIT 4")
    data = cursor.fetchall()
    res = ''

    for row in data:
        res += '{"idimage":' + str(row[0]) + ',"path":"' + str(row[1]) + '"},'

    res = res[:-1]
    print(res)
    result = '{"idtype":"' + str(idt[0]) + '",' \
                                           '"label": "' + str(idt[1]) + '",' \
                                                                        '"images" : [' + res + ']'
    result += '}'
    cursor.close()
    con.close()

    return result


# <------------------ logging tools ------------------>

# Log Textual user actions ( Page loaded , started typing etc ...)
@ application.route('/logaction', methods=['POST'])
def logaction():
    action = request.form['action']
    now, timestamp = gettimes()
    con = mysql.connect()
    cursor = con.cursor()
    idim = request.form['id']
    url = request.form['url']
    idu = getid(request.environ['REMOTE_ADDR'])

    q = "INSERT INTO textvote (iduser,time,date,event,idimage,url) VALUES (" + str(idu) + ",'" + str(
        timestamp) + "','" + str(now) + "','" + action + "'," + str(idim) + ",'" + url + "')"

    cursor.execute(q)
    con.commit()
    cursor.close()
    con.close()
    return 'ok'


@ application.route('/logmultiple', methods=['POST'])
def logmultiple():
    action = request.form['action']
    url = request.form['url']
    now, timestamp = gettimes()
    con = mysql.connect()
    cursor = con.cursor()
    idim = request.form['id']
    idu = getid(request.environ['REMOTE_ADDR'])

    q = "INSERT INTO multiple (iduser,time,date,event,idimage,url) VALUES (" + str(idu) + ",'" + str(
        timestamp) + "','" + str(now) + "','" + action + "'," + str(idim) + ",'" + url + "')"

    cursor.execute(q)
    con.commit()
    cursor.close()
    con.close()
    return 'ok'


@ application.route('/logswipes', methods=['POST'])
def logswipes():
    idimage = request.form['idimg']
    idtype = request.form['idtype']
    url = request.form['url']
    now, timestamp = gettimes()
    idu = getid(request.environ['REMOTE_ADDR'])

    con = mysql.connect()
    cursor = con.cursor()

    q = "INSERT INTO swipe (iduser,`time`,`date`,idimage,idtype,`event`,url) VALUES (" + str(idu) + ",'" + str(
        timestamp) + "','" + str(now) + "','" + str(idimage) + "'," + str(idtype) + ",'visible','" + url + "')"

    cursor.execute(q)
    cursor.close()
    con.commit()
    con.close()
    return 'ok'


@ application.route('/logsel', methods=['POST'])
def logsel():
    idimage = request.form['idimg']
    idtype = request.form['idtype']
    url = request.form['url']
    now, timestamp = gettimes()
    idu = getid(request.environ['REMOTE_ADDR'])

    con = mysql.connect()
    cursor = con.cursor()

    q = "INSERT INTO selection (iduser,`time`,`date`,idimage,idtype,`event`,url) VALUES (" + str(idu) + ",'" + str(
        timestamp) + "','" + str(now) + "','" + str(idimage) + "'," + str(idtype) + ",'page loaded','" + url + "')"

    print(q)

    cursor.execute(q)
    cursor.close()
    con.commit()
    con.close()
    return 'ok'


@ application.route("/logm/<table>", methods=['POST'])
def logm(table):
    idu = getid(request.environ['REMOTE_ADDR'])
    idtype = request.form["idtype"]
    action = request.form["action"]
    url = request.form['url']
    now, timestamp = gettimes()
    idimgs = str(request.form.get('ids')).split(",")
    print(idimgs)
    queries = []

    for image in idimgs:
        print("aaa " + str(image))
        queries.append(
            "INSERT INTO `" + table + "` (iduser,idimage,idtype,`time`,`date`,`event`,url) VALUES(" + str(
                idu) + "," + str(
                image) + "," + str(idtype) + ",'" + str(timestamp) + "','" + str(
                now) + "','" + action + "','" + url + "')")

    con = mysql.connect()
    cursor = con.cursor()
    for q in queries:
        print(q)
        cursor.execute(q)

    cursor.close()
    con.commit()
    con.close()
    return 'ok'


#     <------------------ Admin stats ------------------>

@ application.route("/adminstats")
def adminstats():
    con = mysql.connect()
    cursor = con.cursor()

    tasks = ["textvote", "reverse", "selection", "swipe", "multiple"]
    images = []
    users = []
    classes = []
    skip = []
    result = "{"

    for table in tasks:
        q = "SELECT count(nb) FROM (SELECT count(*) AS nb FROM " + table + " WHERE (event ='submitted' OR event ='chosen' OR event ='swipe')  GROUP BY idimage) AS t"
        cursor.execute(q)
        images.append(cursor.fetchone()[0])

        cursor.execute(
            "SELECT count(nb) FROM (SELECT count(*) AS nb FROM " + table + " WHERE (event ='submitted' OR event ='chosen' OR event ='swipe')  GROUP BY iduser) AS t")
        users.append(cursor.fetchone()[0])

        cursor.execute("SELECT count(*) AS nb FROM " + table + " WHERE event ='skip'")
        skip.append(cursor.fetchone()[0])

        cursor.execute(
            "SELECT count(*) AS nb ,label FROM " + table + " INNER JOIN type ON " + table + ".idtype= type.idtype WHERE (event ='submitted' or event ='chosen' or event ='swipe')  GROUP BY type.idtype ORDER BY  nb DESC LIMIT 4;")
        classes.append(cursor.fetchall())

    cursor.close()
    con.close()

    for i in range(0, len(tasks)):
        if tasks[i] == 'selection':
            skip[i] = int(skip[i] / 6)
        elif tasks[i] == 'reverse':
            skip[i] = int(skip[i] / 4)
        result += '"' + tasks[i] + '"' + ': {"image":"' + str(images[i]) + '","user":"' + str(
            users[i]) + '","skipped":"' + str(skip[i]) + '","classes": [ '

        for cl in classes[i]:
            result += '{"cl": "' + cl[1] + '","nb":"' + str(cl[0]) + '"},'
        result = result[:-1]
        result += ']},'
    result = result[:-1]
    result += "}"
    print(result)

    return result


@ application.route("/getreports")
def getreports():
    con = mysql.connect()
    cursor = con.cursor()
    cols = ["reports", "user", "task", "bug", "image", "path", "url"]
    q = "SELECT idreport,iduser,`where`,label,image.idimage,imagepath,url FROM sql11185116.report INNER JOIN image ON image.idimage = report.idimage"
    data = vachercherm(q)
    res = '['
    for row in data:
        res += '{'
        i = 0
        for col in row:
            res += '"' + cols[i] + '":"' + str(col) + '",'
            i += 1
        res = res[:-1]
        res += '},'
    res = res[:-1]
    res += ']'
    cursor.close()
    con.close()

    return res


@ application.route("/getbasicstats")
def basicstats():
    con = mysql.connect()
    cursor = con.cursor()

    qu = "SELECT count(*) FROM user"
    qi = "SELECT count(*) FROM image"
    qt = "SELECT count(*) FROM type"

    total = "SELECT nb1 +nb2 + nb3 +nb4 +nb5 AS nb  FROM(SELECT count(*) AS nb1 FROM textvote WHERE event ='submitted') AS t1,(SELECT count(*) AS nb2 FROM selection WHERE event ='chosen')AS t2,(SELECT count(*) AS nb3 FROM swipe WHERE event ='swipe') AS t3,(SELECT count(*) AS nb4 FROM reverse WHERE event ='chosen')AS t4,(SELECT count(*) AS nb5 FROM multiple WHERE event ='chosen') AS t5"

    cursor.execute(qu)
    users = cursor.fetchone()[0]

    cursor.execute(qi)
    images = cursor.fetchone()[0]

    cursor.execute(qt)
    types = cursor.fetchone()[0]

    cursor.execute(total)
    saves = cursor.fetchone()[0]

    cursor.close()
    con.close()
    return '{"users": ' + str(users) + ', "images": ' + str(images) + ', "types": ' + str(types) + ', "saves": ' + str(
        saves) + '}'


#     <------------------ Image display info ------------------>



# Display single image tasks in display_image
@ application.route("/getimginfotype", methods=['POST'])
def getimginfotype():
    idimg = request.form['idimg']
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("SELECT count(idimage) AS nbtxt FROM textvote  WHERE idimage=" + str(
        idimg) + " AND idtype IS NOT NULL GROUP BY idimage")
    nbtxt = cursor.fetchone()

    cursor.execute("SELECT count(idimage) AS nbsel FROM selection  WHERE idimage=" + str(
        idimg) + " AND idtype IS NOT NULL  GROUP BY idimage")

    nbsel = cursor.fetchone()
    cursor.execute("SELECT count(idimage) AS nbsw FROM swipe  WHERE idimage=" + str(
        idimg) + "  AND vote IS NOT NULL GROUP BY idimage")

    nbswi = cursor.fetchone()
    cursor.close()
    con.close()

    if nbtxt is None:
        nbtxt = 0
    else:
        nbtxt = nbtxt[0]

    if nbsel is None:
        nbsel = 0
    else:
        nbsel = nbsel[0]
    if nbswi is None:
        nbswi = 0
    else:
        nbswi = nbswi[0]

    return '{"text":"' + str(nbtxt) + '",' \
                                      '"select":"' + str(nbsel) + '",' \
                                                                  '"swipe":"' + str(nbswi) + '"}'


# display to class of a single image Display_image
@ application.route('/topclass', methods=["POST"])
def topclass():
    idimg = request.form['idimg']

    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "SELECT count(idtype),idtype FROM   textvote WHERE idimage =  " + idimg + " AND idtype IS NOT NULL GROUP BY idtype ORDER BY idtype")
    txt = cursor.fetchall()
    cursor.execute(
        "SELECT count(idtype),idtype  FROM selection WHERE idimage = " + idimg + " AND idtype IS NOT NULL GROUP BY idtype ORDER BY idtype")
    sel = cursor.fetchall()
    cursor.execute(
        "SELECT count(idtype),idtype FROM swipe  WHERE idimage =  " + idimg + " AND vote = 1 GROUP BY swipe.idtype ORDER BY idtype")
    swi = cursor.fetchall()

    res = {}

    for row in txt:
        res[str(row[1])] = row[0]

    for row in sel:
        if row is None:
            pass
        else:
            res[str(row[1])] += row[0]

    for row in swi:
        res[str(row[1])] += row[0]

    value = sorted(res.values())[:5]
    print(value)
    print(res)
    result = {}
    for key in res:
        print(value)
        if res[key] in value:
            result[key] = res[key]
            test = True
            for i in range(0, len(value)):
                if value[i] == res[key] and test:
                    value[i] = -36
                    test = False

    print(result.values())

    cursor.close()
    con.close()
    final = '['

    for key in result:
        final += '{"name":"' + getlabel(key) + '",' \
                                               '"value":"' + str(result[key]) + '"},'

    final = final[:-1]
    return final + ']'

    # index


#     <------------------ Image access ------------------>



# Return Image path from given ID used in display_image
@ application.route('/getimgbyid', methods=['POST'])
def getimgbyid():
    action = request.form['action']
    result = '['
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT DISTINCT imagepath,idimage FROM image WHERE idimage =" + str(action))
    data = cursor.fetchall()
    for row in data:
        result += '{"path": "' + str(row[0]) + '","idimage":' + str(row[1]) + '},'

    result = result[:-1]

    result += ']'

    cursor.close()
    con.close()
    return json.dumps(result)


# Get image from given type with SQL match (LIKE %%) used in display_image
@ application.route('/getimgbytype', methods=['POST'])
def getimgbytype():
    action = request.form['action']
    result = []
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "SELECT DISTINCT imagepath,image.idimage FROM image INNER  JOIN textvote ON image.idimage= textvote.idimage INNER JOIN type  ON type.idtype= textvote.idtype WHERE label LIKE '%" + str(
            action) + "%'")
    data = cursor.fetchall()

    result = '['

    for row in data:
        result += '{"path": "' + str(row[0]) + '","id":' + str(row[1]) + '},'

    result = result[:-1]
    result += ']'
    print(result)

    cursor.close()
    con.close()
    return json.dumps(result)


#     <------------------- Chrome app saving ------------------>
@ application.route("/saveapp", methods=["POST"])
def saveapp():
    idu = getid(request.environ["REMOTE_ADDR"])
    file = request.files['local']
    s3_client = boto3.client('s3')

    _, now = gettimes()

    fileurl = 'https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/app/' + str(
        idu) + "_" + str(now) + ".png"

    putdb("INSERT INTO image (imagepath,`from`) VALUES ('" + fileurl + "','app')")

    idm = vachercherss("SELECT idimage FROM image WHERE imagepath LIKE '" + fileurl + "'")

    # Upload the file to S3
    s3_client.upload_fileobj(file, 'namethatchart-imagedataset', "app/" + str(idu) + "_" + str(now) + ".png",
                             ExtraArgs={'ACL': 'public-read'})

    return "<strong>Your image id is : " + str(
        idm) + ". \n</strong></br></br>" + "Please keep this number in order to tack this image. It is available : <a href='https://namethatchart.herokuapp.com/display_image/'" + str(
        idm) + ">Our dataset display</a>"


#     <------------------- Dataset download ------------------>
@ application.route("/datcsv.csv")
def dattcsv():
    header = "task,task_id,iduser,timestamp,date,event,idtype,label,idimg,imagepath,url\n"
    body = ""
    db = []
    db.append(vachercherm(
        "SELECT 'textual'AS task,concat('textual_',idtextvote),iduser,time,date,event,textvote.idtype,label,image.idimage,imagepath,url FROM textvote INNER JOIN image ON textvote.idimage = image.idimage INNER JOIN type ON textvote.idtype = type.idtype"))
    db.append(vachercherm(
        "SELECT 'reverse' AS task, concat('reverse_',idreverse),iduser,time,date,event,reverse.idtype,label,image.idimage,imagepath,url FROM reverse INNER JOIN image ON reverse.idimage = image.idimage INNER JOIN type ON reverse.idtype = type.idtype"))
    db.append(vachercherm(
        "SELECT 'selection' AS task,concat('selection_',idselection),iduser,time,date,event,selection.idtype,label,image.idimage,imagepath,url FROM selection INNER JOIN image ON selection.idimage = image.idimage INNER JOIN type ON selection.idtype = type.idtype"))
    db.append(vachercherm(
        "SELECT 'swipe' AS task,concat('swipe_',idswipe),iduser,time,date,event,swipe.idtype,label,image.idimage,imagepath,url FROM swipe INNER JOIN image ON swipe.idimage = image.idimage INNER JOIN type ON swipe.idtype = type.idtype"))

    for table in db:
        for row in table:
            for col in row:
                body += str(col) + ","
            body = body[:-1] + "\n"
    return Response(header + body, mimetype="text/csv",
                    headers={"Content-disposition": "attachment; filename=data.csv"})


#     <------------------- Image / JSON upload & JSON demo ------------------>
# Save upload of image (admin) with FORM
@ application.route('/saveupimg', methods=['POST'])
def saveupimg():
    url = request.form['url']

    _, now = gettimes()
    idu = getid(request.environ["REMOTE_ADDR"])

    name = wget.detect_filename(url)
    temp = name.split('.')

    ext = str(temp[len(temp) - 1])

    filename = str(idu) + "_" + str(now) + "." + ext

    q = os.path.join(os.getcwd(), "static/assets/img/datasets/json/" + filename)

    wget.download(url, q)
    s3_client = boto3.client('s3')
    with open(q, "rb") as f:
        s3_client.upload_fileobj(f,
                                 'namethatchart-imagedataset', "upload/" + str(idu) + "_" + str(now) + "." + ext,
                                 ExtraArgs={'ACL': 'public-read'})

    fileurl = 'https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/upload/' + str(
        idu) + "_" + str(now) + "." + ext

    query = "INSERT INTO image (imagepath,`from`) VALUES ('" + fileurl + "','upload')"
    putdb(query)

    return redirect("/uploadimg?m=dGV4dHV")


# Save upload of image (admin) with JSON
@ application.route("/upjsonimg", methods=['POST'])
def upjonimg():
    images = ["png", "jpeg", "jpg", "svg"]

    file = request.files['file']
    tempu = file.filename

    tempr = tempu.split('.')

    ext = str(tempr[len(tempr) - 1]).lower()
    _, now = gettimes()
    idu = getid(request.environ["REMOTE_ADDR"])
    fileurl = 'https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/upload/' + str(
        idu) + "_" + str(now)

    s3_client = boto3.client('s3')

    if ext in images:

        putdb("INSERT INTO image (imagepath,`from`) VALUES ('" + fileurl + "." + ext + "','app')")

        # Upload the file to S3
        s3_client.upload_fileobj(file, 'namethatchart-imagedataset', "upload/" + str(idu) + "_" + str(now) + "." + ext,
                                 ExtraArgs={'ACL': 'public-read'})
    else:
        if ext != 'json':
            return 'Must be a picture or json file', 403
        try:
            filestring = ""
            for line in file:
                filestring += str(line)[2:][:-3]

            data = json.loads(filestring)

            print(len(data))
            for obj in data:
                if "url" in obj:

                    nb = len(pics.getimgs("./static/assets/img/datasets/json/")) + 2
                    print(obj)
                    name = wget.detect_filename(obj['url'])
                    temp = name.split('.')
                    ext = str(temp[len(temp) - 1])
                    if "title" in obj:
                        title = obj["title"].replace(" ", "_")
                        filename = str(nb) + "_" + title + "." + ext
                    else:
                        title = ""
                        filename = str(nb) + "." + ext

                    wget.download(obj['url'], os.path.join(os.getcwd(), "static/assets/img/datasets/json/" + filename))

                    s3_client = boto3.client('s3')
                    with open(os.path.join(os.getcwd(), "static/assets/img/datasets/json/" + filename), "rb") as f:
                        _, now = gettimes()
                        s3_client.upload_fileobj(f, 'namethatchart-imagedataset',
                                                 "upload/" + str(idu) + "_" + str(now) + "." + ext,
                                                 ExtraArgs={'ACL': 'public-read'})

                    url = "https://s3.eu-central-1.amazonaws.com/namethatchart-imagedataset/upload/" + str(
                        idu) + "_" + str(
                        now) + "." + ext

                    if 'category' in obj:
                        if 'difficulty' in obj:
                            query = "INSERT INTO image (imagepath,`from`,title,category,difficulty) VALUES ('" + url + "','upload','" + title + "','" + \
                                    obj['category'] + "','" + obj["difficulty"] + "')"
                        else:
                            query = "INSERT INTO image (imagepath,`from`,title,category) VALUES ('" + url + "','upload','" + title + "','" + \
                                    obj['category'] + "')"
                    else:
                        query = "INSERT INTO image (imagepath,`from`,title) VALUES ('" + url + "','upload','" + title + "')"

                    putdb(query)
                else:
                    return 'invalid json', 400
        except Exception as e:
            if 'timeout' in str(e):
                return 'connexion timeout', 502
            elif 'string indices must be integers' in str(e):
                return 'invalid url', 403
            return 'invalid jsons', 400
    return 'Uploaded', 200


@ application.route('/demo.json')
def demojson():
    res = ""
    with open(os.path.join(os.getcwd(), "static/assets/json/demo.json"), "r") as f:
        for line in f:
            res += str(line.rstrip())

    response = app.response_class(
        response=json.dumps(res).replace("\\", "")[:-1][1:],
        status=200,
        mimetype='application/json'
    )
    return response


# <------------------ Classic methods ------------------>

def getid(ip):
    if "first" not in session:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("INSERT INTO user (ipuser) VALUES ('" + ip + "')")
        cursor.close()
        con.commit()
        cursor = con.cursor()
        cursor.execute("SELECT max(iduser) FROM user WHERE ipuser ='" + ip + "'")
        data = cursor.fetchone()[0]
        cursor.close()
        con.close()
        session["first"] = False
        session["id"] = data

        return data
    else:
        print(session["id"])
        return session["id"]


def gettype(typename):
    con = mysql.connect()
    cursor = con.cursor()
    typename = typename.lower()

    if " " in typename:
        typename = typename.replace(" ", "_")

    q = "SELECT idtype FROM type WHERE lower(label) LIKE '" + typename + "'"
    cursor.execute(q)
    data = cursor.fetchone()
    if data is None:
        query = "INSERT INTO type (label) VALUES ('" + typename.replace("_", " ") + "')"
        cursor.execute(query)
        con.commit()
    cursor.execute("SELECT idtype FROM type WHERE lower(label) LIKE '" + typename.replace("_", " ") + "'")
    data = cursor.fetchone()
    cursor.close()
    con.close()
    return data


def to_bool(s):
    return 1 if s == 'true' else 0


def gettimes():
    now = datetime.datetime.now()
    timestamp = str(time.mktime(now.timetuple())).replace(".0", "")
    return str(now)[:-3], timestamp


def getcost(task, lvl):
    if lvl == 2:
        if task == 0:
            cost = -10
        elif task == 1:
            cost = -5
        else:
            cost = + 60
    elif lvl == 1:
        if task == 0:
            cost = -15
        elif task == 1:
            cost = -10
        else:
            cost = + 40
    else:
        if task == 0:
            cost = -25
        elif task == 1:
            cost = -15
        else:
            cost = +45
    print(str(cost) + "COUT")
    return cost


def getlvl(ip):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT lvl,iduser,taskforce FROM user WHERE ipuser ='" + ip + "'")
    data = cursor.fetchone()
    session["lvl"] = data[0]
    session["id"] = data[1]
    session["task"] = data[2]

    return data[0]


def getlabel(id):
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("SELECT label FROM type WHERE idtype = " + str(id))
    data = cursor.fetchone()[0]

    return data


def vachercherm(query):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    con.close()

    return result


def vacherchers(query):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    con.close()

    return result


def putdb(query):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(query)
    cursor.close()
    con.commit()
    con.close()


def vachercherss(query):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    con.close()

    return result[0]


# only  non used methods
"""                         OLD                                """


# Preview of user D3JS integration
@ application.route('/preview')
def preview():
    return render_template('preview.html')


# Mapping of d3js files to display them into textual
@ application.route('/textual/<chart>')
def generic(chart):
    return render_template(chart)


# Mapping of d3js files to display them into preview
@ application.route('/preview/<chart>')
def genericprev(chart):
    return render_template("preview/" + chart + '.html')


# View of textual ( both d3js & images)
@ application.route('/hybrid')
def hybrid():
    a = randint(0, 100)
    if a > 50:
        return render_template("textual.html")
    else:
        return render_template('textualimg.html')


def getrandomdataint():
    nbclasse = randint(3, 16)
    result = {'res': []}
    for i in range(0, nbclasse):
        result['res'].append({"key": randint(3, 8000), "name": "foo" + str(i)})
    return json.dumps(result)


def getposted(id):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT posted FROM user WHERE iduser = " + str(id) + " LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    con.close()
    return data[0]


# fill database from "/static/assets/img/datasets/"
@ application.route('/maj/<dir>/<nb>')
def maj(dir, nb):
    pathdir = "assets/img/datasets/downloadApi/" + dir + "/"
    imgs = pics.getimgs("./static/" + pathdir)
    con = mysql.connect()
    cursor = con.cursor()
    y = 0
    for i in range(0, len(imgs)):
        try:
            temp = Image.open(imgs[i])
            width, height = temp.size
            if width < 400:
                os.remove(img.path)
            else:
                path = imgs[i].replace("./static/", "")
                temp = path.split('_')
                ext = str(temp[0])
                idtype = gettype(ext.replace(pathdir, ""))[0]

                cursor.execute("SELECT * FROM image WHERE imagepath LIKE '" + path + "' LIMIT 1")
                data = cursor.fetchone()

                if data is None:
                    cursor.execute(
                        "INSERT INTO image (imagepath,`from`,idtype) VALUES ('" + path + "','" + dir + "'," + str(
                            idtype) + ")")

        except Exception as e:
            print(e)
            os.remove(imgs[i])
            y += 1

    cursor.close()
    con.commit()
    con.close()

    print('\x1b[6;30;42m' + "Done ! (" + str(len(imgs) - y) + "/" + str(len(imgs)) + ") saved out of the " + str(
        nb) + " initial" '\x1b[0m' + "\n")

    return "ok"


# Save Generated Chart from Textual (D3JS)
@ application.route('/saveimg', methods=['POST'])
def saveimg():
    result = request.files['local']
    img = Image.open(result)
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, img)
    con = mysql.connect()
    cursor = con.cursor()
    nb = len(pics.getimgs("./static/assets/img/datasets/textualsaved/")) + 2
    path = "assets/img/datasets/textualsaved/" + str(nb) + ".jpg"
    bg.save("./static/" + path)

    cursor.execute(
        "INSERT INTO image (imagepath,`from`,category,difficulty) VALUES ('" + path + "','generated','standard','0')")
    con.commit()
    query = "SELECT idimage FROM image WHERE imagepath = '" + path + "'"
    cursor.execute(query)
    session['idimg'] = cursor.fetchone()[0]

    cursor.close()
    con.close()
    return 'ok'


"""  ADMIN TOOLS
@ application.route("/tempdl/<dir>/<filename>")
def tempdl(dir, filename):
    location = "static/assets/img/datasets/downloadApi/" + dir + "/"
    nb = rd.getimgtypes(location, filename)

    return redirect("../maj/" + dir + "/" + str(nb))


# get d3js html from bl.ock and save it
@ application.route('/gethemall')
def gethemall():
    views = dl.parsej()
    con = mysql.connect()
    cursor = con.cursor()
    for view in views:
        idt = gettype(view.description)[0]
        q = "INSERT INTO user_type VALUES (" + str(4) + "," + str(
            idt) + ",'" + view.getlocation() + "','" + view.name + "')"
        ursor.execute(q)
        con.commit()
    cursor.close()
    con.close()
    return '<h3> done to:' + str(len(views)) + "visualizations  </h3>"


# download thumbnails and save them
@ application.route('/downthumb')
def downthumb():
    views = dl.getthumb()
    # for view in views:
    # idt = gettype(view.description)[0]
    # cursor.execute(q)

    return '<h3> done to : ' + str(len(views)) + "visualizations  </h3>"


@ application.route('/indabase/<dir>')
def indabase(dir):
    pathdir = "assets/img/datasets/downloadApi/" + dir + "/"
    imgs = pics.getimgs("./static/" + pathdir)
    con = mysql.connect()
    cursor = con.cursor()
    y = 0
    for i in range(0, len(imgs)):

        path = imgs[i].replace("./static/", "")

        cursor.execute("SELECT * FROM image WHERE imagepath LIKE '" + path + "' LIMIT 1")
        data = cursor.fetchone()

        if data is None:
            cursor.execute(
                "INSERT INTO image (imagepath,`from`) VALUES ('" + path + "','" + dir + "')")

    cursor.close()
    con.commit()
    con.close()

    print('\x1b[6;30;42m' + "Done ! " + str(len(imgs)) + ") saved " + '\x1b[0m' + "\n")

    return "ok" """

"""      Get data           """


# Return User data to display into admin table
@ application.route('/userstats')
def getskip():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(
        "SELECT count(user.iduser),event,user.iduser,posted FROM textvote INNER JOIN user ON user.iduser = textvote.iduser WHERE event='skip'GROUP BY user.iduser ORDER BY posted DESC,iduser ASC")
    skip = cursor.fetchall()

    cursor.execute(
        "SELECT count(user.iduser),event,user.iduser,posted FROM textvote INNER JOIN user ON user.iduser = textvote.iduser WHERE event='submitted' GROUP BY user.iduser ORDER BY posted DESC,iduser ASC")
    sub = cursor.fetchall()

    cursor.execute(
        "SELECT idimage,date,user.iduser,posted FROM textvote INNER JOIN user ON user.iduser = textvote.iduser WHERE event='page loaded' ORDER BY posted DESC,iduser,idimage ASC")
    pl = cursor.fetchall()

    cursor.execute(
        "SELECT idimage,date,user.iduser,posted FROM textvote INNER JOIN user ON user.iduser = textvote.iduser WHERE event='skip' ORDER BY posted DESC,iduser,idimage ASC")
    skipd = cursor.fetchall()

    cursor.execute(
        "SELECT idimage,date,user.iduser,posted FROM textvote INNER JOIN user ON user.iduser = textvote.iduser WHERE event='submitted' ORDER BY posted DESC,iduser,idimage ASC")
    subd = cursor.fetchall()
    a, b = getavg(pl, skipd, subd)
    res = []
    i = 0

    for us in skip:

        if i < len(a):
            suba = a[i]
        else:
            suba = 0

        if i < len(b):
            skipa = b[i]
        else:
            skipa = 0

        res.append({'id': us[2], 'posted': us[3], 'skipped': us[0], 'submitted': sub[i][0],
                    'averageSub': "{0:.2f}".format(suba), 'averageSkip': "{0:.2f}".format(skipa)})
        i = i + 1
    cursor.close()
    con.close()
    return json.dumps(res)


# admin textual stat (pie chart)
@ application.route('/firstrow')
def getfirstrow():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(
        "SELECT type.idtype,label,count(type.idtype) AS nb FROM type,textvote WHERE type.idtype = textvote.idtype GROUP BY type.idtype, label ORDER BY  nb  DESC LIMIT 4;")
    data = cursor.fetchall()
    cursor.close()
    con.close()
    return json.dumps(data)


# Save early information of a preview
@ application.route('/presaveviz', methods=['POST'])
def presaveviz():
    file = request.files['local']
    name = request.form['type']
    id = getid(request.environ['REMOTE_ADDR'])
    nb = getposted(id) + 1
    session['type'] = name
    session['nb'] = nb
    session['filename'] = str(id) + "_" + str(nb)
    file.save("./templates/preview/" + str(id) + "_" + str(nb) + ".html")

    con = mysql.connect()
    cursor = con.cursor()
    q = "UPDATE user SET posted = " + str(nb) + " WHERE iduser = " + str(id)
    cursor.execute(q)
    con.commit()
    cursor.close()
    con.close()
    return "../preview"


# Actual saving of a preview
@ application.route('/savepreview')
def savepreview():
    name = session.get('filename') + ".html"
    os.rename(os.path.join(os.getcwd(), "templates/preview/" + name), os.path.join(os.getcwd(), "templates/" + name))
    idt = gettype(session.get('type'))[0]
    idu = getid(request.environ['REMOTE_ADDR'])

    con = mysql.connect()
    cursor = con.cursor()
    q = "INSERT INTO user_type (iduser,idtype,url) VALUES (" + str(idu) + "," + str(idt) + ",'" + str(name) + "')"
    cursor.execute(q)

    cursor.close()
    con.commit()
    con.close()

    return 'ok'


# Return filename stored in session (upload D3JS)
@ application.route('/getinfo')
def getinf():
    return session.get('filename')


# Group user rows and make average of time
def getavg(page, skip, sub):
    old = None
    skiptot = 0
    subtot = 0
    subresult = []
    skipresult = []
    skipi = 0
    subi = 0
    nbsk = 0
    nbsb = 0

    for val in page:
        if old is None:
            old = val[2]

        if old == val[2]:
            if val[0] == sub[subi][0]:
                subtot += (
                              datetime.datetime.strptime(sub[subi][1],
                                                         "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                                  val[1],
                                  "%Y-%m-%d %H:%M:%S.%f")).total_seconds() * 1000
                if subi + 1 < len(sub):
                    subi += 1
                nbsb += 1

            elif val[0] == skip[skipi][0]:
                skiptot += (
                               datetime.datetime.strptime(skip[skipi][1],
                                                          "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                                   val[1],
                                   "%Y-%m-%d %H:%M:%S.%f")).total_seconds() * 1000

                if skipi + 1 < len(skip):
                    skipi += 1
                nbsk += 1
        else:
            if nbsb > 0:
                subresult.append(subtot / nbsb)

            if nbsk > 0:
                skipresult.append(skiptot / nbsk)

            skiptot = 0
            subtot = 0

            nbsk = 0
            nbsb = 0

            if val[0] == sub[subi][0]:
                subtot += (
                              datetime.datetime.strptime(sub[subi][1],
                                                         "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                                  val[1],
                                  "%Y-%m-%d %H:%M:%S.%f")).total_seconds() * 1000
                if len(sub) > subi + 1:
                    subi += 1
                nbsb = 1


            elif skip[skipi] == val[0]:
                skiptot += (
                               datetime.datetime.strptime(skip[skipi][1],
                                                          "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                                   val[1],
                                   "%Y-%m-%d %H:%M:%S.%f")).total_seconds() * 1000
                if skipi + 1 < len(skip):
                    skipi += 1
                nbsk = 1
        if len(subresult) == 0:
            if nbsb > 0:
                subresult.append(subtot / nbsb)

        if nbsk > 0:
            skipresult.append(skiptot / nbsk)

    return subresult, skipresult


#     <------------------ Dataset generator ------------------>

# get data like {"a": 45}
@ application.route('/1data')
def getrandomintjson():
    return getrandomdataint()


# get data like {'val1':5 'val2':45}
@ application.route('/2data')
def getrandom2djson():
    nbclasse = randint(3, 180)
    result = {'res': []}
    pred = 0
    for i in range(0, nbclasse):
        value = pred + randint(3, 200)
        pred = value
        result['res'].append({"val1": value, "val2": randint(3, 160000)})
    return json.dumps(result)


# <------------------ Textual tools ------------------>

# Get HTML D3JS file to load into textual
@ application.route('/getnext')
def getnext():
    con = mysql.connect()
    cursor = con.cursor()
    if session.get('last') is None:

        cursor.execute("SELECT url,idtype FROM user_type ORDER BY RAND() LIMIT 1")
    else:
        cursor.execute("SELECT url,idtype FROM user_type WHERE NOT idtype='" + str(
            session.get('last')) + "' ORDER BY RAND() LIMIT 1")
    data = cursor.fetchone()

    session['last'] = data[1]
    cursor.close()
    con.close()
    return data[0]


# View to upload D3JS Files
@ application.route('/upload')
def upload():
    return render_template('upload.html')


if __name__ == '__main__':
    application.debug = True
    application.run()

