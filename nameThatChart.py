import binascii
import json
import os
from random import randint

from PIL import Image
from flask import Flask, request, session, render_template
from possibleview import View
import d3jsdownload as dl
import datetime
import time

from flaskext.mysql import MySQL

import imagePrep as pics

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'sql11185116'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hULHvUiMJh'
app.config['MYSQL_DATABASE_DB'] = 'sql11185116'
app.config['MYSQL_DATABASE_HOST'] = 'sql11.freemysqlhosting.net'
mysql.init_app(app)

# hash key
app.secret_key = binascii.hexlify(os.urandom(24))


#     <------------------Admin unmap tools ------------------>

# get d3js html from bl.ock and save it
@app.route('/gethemall')
def gethemall():
    views = dl.parsej()
    con = mysql.connect()
    cursor = con.cursor()
    for view in views:
        idt = gettype(view.description)[0]
        q = "INSERT INTO user_type VALUES (" + str(4) + "," + str(
            idt) + ",'" + view.getlocation() + "','" + view.name + "')"
        print(q)
        cursor.execute(q)
        con.commit()
    cursor.close()
    con.close()
    return '<h3> done to:' + str(len(views)) + "visualizations  </h3>"


# download thumbnails and save them
@app.route('/downthumb')
def downthumb():
    views = dl.getthumb()
    # for view in views:
    # idt = gettype(view.description)[0]
    # cursor.execute(q)

    return '<h3> done to : ' + str(len(views)) + "visualizations  </h3>"


# fill database from "/static/assets/img/datasets/"
@app.route('/maj')
def maj():
    imgs = pics.getimgs("./static/assets/img/datasets/")
    con = mysql.connect()
    cursor = con.cursor()

    for i in range(0, len(imgs)):
        path = imgs[i].replace("./static/", "")
        cursor.execute("SELECT * FROM image WHERE imagepath LIKE '%" + path + "%' LIMIT 1")
        data = cursor.fetchone()

        if data is None:
            cursor.execute("INSERT INTO image (imagepath) VALUES ('" + path + "')")

    cursor.close()
    con.commit()
    con.close()
    return "ok"


#     <------------------ Classic render template ------------------>

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/multiple')
def temp():
    return render_template('multiple.html')


@app.route('/textual')
def textual():
    return render_template('textual.html')


@app.route('/test')
def test():
    return render_template('biovisualize:_Simple_Binary_Tree.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/hum')
def hum():
    return render_template('preview/1_7.html')


@app.route('/preview')
def preview():
    return render_template('preview.html')


@app.route('/textual/<chart>')
def generic(chart):
    return render_template(chart)


@app.route('/preview/<chart>')
def genericprev(chart):
    return render_template("preview/" + chart + '.html')


@app.route('/display_image')
def display_image():
    return render_template('display_image.html')


#     <------------------ Dataset generator ------------------>


# get data like "a" 45
@app.route('/1data')
def getrandomintjson():
    return getrandomdataint()


# get data like val1:5 val2:45
@app.route('/2data')
def getrandom2djson():
    nbclasse = randint(3, 180)
    result = {'res': []}
    pred = 0
    for i in range(0, nbclasse):
        value = pred + randint(3, 200)
        pred = value
        result['res'].append({"val1": value, "val2": randint(3, 160000)})
    return json.dumps(result)


#     <------------------ Save of exercices ------------------>

@app.route('/savemultiple', methods=['POST'])
def savemultiple():
    name = request.form.get("name")
    name = str(name.replace("\n", ""))
    name = str(name.replace("_", " "))

    url = request.form.get("url")
    con = mysql.connect()
    cursor = con.cursor()

    q1 = "SELECT idimage FROM image WHERE imagepath = '" + url.replace("/static/", "") + "'"
    q2 = "SELECT idtype FROM type WHERE label = '" + name + "'"
    cursor.execute(q1)
    idm = cursor.fetchone()
    cursor.execute(q2)
    idt = cursor.fetchone()
    idu = getid(request.environ['REMOTE_ADDR'])

    cursor.execute("SELECT iduser FROM multiplevote WHERE iduser=" + str(idu[0]) + " AND idimage =" + str(idm[0]) + "")
    data = cursor.fetchone()

    if data is None:
        final = "INSERT INTO multiplevote (iduser,idimage,idtype) VALUES (" + str(idu[0]) + "," + str(
            idm[0]) + "," + str(
            idt[0]) + ")"
    else:
        final = "UPDATE multiplevote SET idtype =" + str(idt[0]) + " WHERE iduser=" + str(
            idu[0]) + " AND idimage =" + str(idm[0])
    print(final)
    cursor.execute(final)
    cursor.close()
    con.commit()
    con.close()
    return 'ok'


@app.route('/savetext', methods=['POST'])
def savetext():
    name = request.form["name"]

    now, timestamp = gettimes()

    con = mysql.connect()
    cursor = con.cursor()

    idim = session.get('idimg')
    idu = getid(request.environ['REMOTE_ADDR'])[0]
    idt = gettype(name)[0]

    query = "INSERT INTO textvote (iduser,time,date,event,idtype,idimage) VALUES(" + str(idu) + ",'" + str(
        timestamp) + "','" + str(now) + "','" + "submitted" + "'," + str(idt) + "," + str(idim) + ")"

    cursor.execute(query)
    con.commit()

    cursor.close()
    con.close()

    return 'ok'


#     <------------------ Mapped admin tools ------------------>

@app.route('/getinfo')
def getinf():
    return session.get('filename')


@app.route('/presaveviz', methods=['POST'])
def presaveviz():
    file = request.files['local']
    print(file.filename)
    name = request.form['type']
    id = getid(request.environ['REMOTE_ADDR'])[0]
    nb = getposted(id) + 1
    print(name)
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


@app.route('/savepreview')
def savepreview():
    name = session.get('filename') + ".html"
    os.rename(os.path.join(os.getcwd(), "templates/preview/" + name), os.path.join(os.getcwd(), "templates/" + name))
    print(session.get('type'))
    idt = gettype(session.get('type'))[0]
    idu = getid(request.environ['REMOTE_ADDR'])[0]

    con = mysql.connect()
    cursor = con.cursor()
    q = "INSERT INTO user_type (iduser,idtype,url) VALUES (" + str(idu) + "," + str(idt) + ",'" + str(name) + "')"
    print(q)
    cursor.execute(q)

    cursor.close()
    con.commit()
    con.close()

    return 'ok'


# admin textual stat
@app.route('/firstrow')
def getfirstrow():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(
        "SELECT type.idtype,label,count(type.idtype) AS nb FROM type,textvote WHERE type.idtype = textvote.idtype GROUP BY type.idtype, label ORDER BY  nb  DESC LIMIT 4;")
    data = cursor.fetchall()
    cursor.close()
    con.close()
    return json.dumps(data)

    return getrandomdataint()


# Export database
@app.route('/db2csv')
def db2csv():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute(
        "SELECT idtextvote,user.iduser,ipuser,time,date,event,image.idimage,label FROM textvote INNER JOIN image ON "
        + "image.idimage = textvote.idimage INNER JOIN user ON textvote.iduser=user.iduser LEFT JOIN type ON textvote.idtype=type.idtype")
    data = cursor.fetchall()
    res = "["
    for i in range(0, len(data)):
        stra = "[ "
        for y in range(0, len(data[0])):
            stra += "'" + str(data[i][y]) + "'"
            if y != len(data[0]) - 1:
                stra += ","

        stra += "]"
        if i != len(data) - 1:
            stra += ","
        res += stra
    res += " ]"
    cursor.close()
    con.close()
    print(json.dumps(res))
    return res


#     <------------------ Textual tools ------------------>


@app.route('/getnext')
def getnext():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT url FROM user_type  ORDER BY RAND() LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    con.close()
    return data


@app.route('/saveimg', methods=['POST'])
def saveimg():
    result = request.files['local']
    img = Image.open(result)
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, img)
    nb = len(pics.getimgs("./static/assets/img/datasets/textualsaved/")) + 2
    path = "assets/img/datasets/textualsaved/" + str(nb) + ".jpg"
    print(path)
    bg.save("./static/" + path)

    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("INSERT INTO image (imagepath) VALUES ('" + path + "')")
    con.commit()
    query = "SELECT idimage FROM image WHERE imagepath = '" + path + "'"
    print(query)
    cursor.execute(query)
    session['idimg'] = cursor.fetchone()[0]

    cursor.close()
    con.close()
    return 'ok'


@app.route('/logaction', methods=['POST'])
def logaction():
    action = request.form['action']
    now, timestamp = gettimes()
    con = mysql.connect()
    cursor = con.cursor()
    idim = session.get('idimg')
    idu = getid(request.environ['REMOTE_ADDR'])[0]

    q = "INSERT INTO textvote (iduser,time,date,event,idimage) VALUES (" + str(idu) + ",'" + str(
        timestamp) + "','" + str(now) + "','" + action + "'," + str(idim) + ")"

    cursor.execute(q)
    con.commit()
    cursor.close()
    con.close()
    return 'ok'

    # <------------------ Unmapped Get ------------------>


#     <------------------ Image tools ------------------>

@app.route('/getimgbyid', methods=['POST'])
def getimgbyid():
    action = request.form['action']
    result = []
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("SELECT imagepath FROM image WHERE idimage =" + str(action))
    data = cursor.fetchall()
    print("lllllaaaa")
    for i in range(0, len(data)):
        result.append("static/" + str(data[i][0]))

    cursor.close()
    con.close()
    return json.dumps(result)


@app.route('/getimgbytype', methods=['POST'])
def getimgbytype():
    action = request.form['action']
    result = []
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "SELECT imagepath FROM image INNER  JOIN textvote ON image.idimage= textvote.idimage INNER JOIN type  ON type.idtype= textvote.idtype WHERE label LIKE '%" + str(
            action) + "%'")
    data = cursor.fetchall()
    for i in range(0, len(data)):
        result.append("static/" + str(data[i][0]))

    cursor.close()
    con.close()
    return json.dumps(result)


def getposted(id):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT posted FROM user WHERE iduser = " + str(id) + " LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    con.close()
    return data[0]


def getid(ip):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT ipuser FROM user WHERE ipuser ='" + ip + "'")
    data = cursor.fetchone()

    if data is None:

        cursor.execute("INSERT INTO user (ipuser) VALUES ('" + ip + "')")
        cursor.close()
        con.commit()
        cursor = con.cursor()
        cursor.execute("SELECT iduser FROM user WHERE ipuser ='" + ip + "'")
        data = cursor.fetchone()
        cursor.close()
        con.close()
        return data
    else:
        print("LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        query = "SELECT iduser FROM user WHERE ipuser ='" + ip + "'"
        cursor.execute(query)
        data = cursor.fetchone()
        con.close()
        return data


def getrandomdataint():
    nbclasse = randint(3, 16)
    result = {'res': []}
    for i in range(0, nbclasse):
        result['res'].append({"key": randint(3, 8000), "name": "foo" + str(i)})
    return json.dumps(result)


def gettype(typename):
    con = mysql.connect()
    cursor = con.cursor()
    typename = typename.lower()

    if " " in typename:
        typename = typename.replace(" ", "_")

    q = "SELECT idtype FROM type WHERE lower(label) LIKE '" + typename + "'"
    print(q)
    cursor.execute(q)
    data = cursor.fetchone()
    if data is None:

        if "chart" in typename:
            if "_chart" in typename or "-chart" in typename or ".chart" in typename:
                typename = typename.replace("_", "chart")
                typename = typename.replace("-", "chart")
                typename = typename.replace(".", "chart")
            else:
                typename = typename.replace("chart", "_chart")
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


def gettimes():
    now = datetime.datetime.now()
    timestamp = str(time.mktime(now.timetuple())).replace(".0", "")
    return str(now)[:-3], timestamp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run()
