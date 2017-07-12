import binascii
import json
import os
from random import randint
from PIL import Image
from flask import Flask, request, session, render_template
from possibleview import View
import d3jsdownload as dl

from flaskext.mysql import MySQL

import imagePrep as pics

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'bb4f44ef9e9757'
app.config['MYSQL_DATABASE_PASSWORD'] = '0cf02e4a'
app.config['MYSQL_DATABASE_DB'] = 'heroku_fe2750702799a19'
app.config['MYSQL_DATABASE_HOST'] = 'eu-cdbr-west-01.cleardb.com'
mysql.init_app(app)

#hash key
app.secret_key = binascii.hexlify(os.urandom(24))

@app.route('/gethemall')
def gethemall():
    views = dl.parsej()
    con = mysql.connect()
    cursor = con.cursor()
    for view in views:
        idt = gettype(view.description)[0]
        q= "insert into user_type values ("+str(4)+","+str(idt)+",'"+view.getlocation()+"','"+view.name+"')"
        print(q)
        cursor.execute(q)
        con.commit()
    cursor.close()
    con.close()
    return '<h3> done to:' + str(len(views)) + "visualizations </h3>"




@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/multiple')
def temp():
    return render_template('multiple.html')


@app.route('/textual')
def textual():
    return render_template('textual.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/preview')
def preview():
    return render_template('preview.html')


@app.route('/textual/<chart>')
def generic(chart):
    return render_template(chart)


@app.route('/preview/<chart>')
def genericprev(chart):
    return render_template("preview/" + chart + '.html')


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


@app.route('/getimg')
def getimg():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT imagepath FROM image ORDER BY RAND() LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    con.close()

    return data


@app.route('/getnext')
def getnext():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT url FROM user_type  ORDER BY RAND() LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    con.close()
    return data


def getposted(id):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT posted FROM user WHERE iduser = " + str(id) + " LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    con.close()
    return data[0]


@app.route('/savetext', methods=['POST'])
def savetext():
    result = request.files['local']
    name = request.form["name"]
    img = Image.open(result)
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, img)
    path = "assets/img/datasets/" + str(len(pics.getimgs("./static/assets/img/datasets/")) + 2) + ".jpg"
    bg.save("./static/" + path)

    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("INSERT INTO image (imagepath) VALUES ('" + path + "')")
    con.commit()
    print(session.get('id'))
    cursor.execute("SELECT idimage FROM image WHERE imagepath = '" + path + "'")
    idim = cursor.fetchone()[0]
    idu = getid(request.environ['REMOTE_ADDR'])[0]
    idt = gettype(name)[0]

    query = "INSERT INTO textvote VALUES(" + str(idu) + "," + str(idim) + "," + str(idt) + ")"
    print(query)
    cursor.execute(query)
    con.commit()

    cursor.close()
    con.close()

    return 'ok'

#Export database
@app.route('/db2csv')
def db2csv():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT image,label FROM textvote INNER JOIN type ON type=idtype ORDER BY image")
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


@app.route('/savepreview')
def savepreview():
    name = session.get('filename') + ".html"
    os.rename(os.path.join(os.getcwd(), "templates/preview/" + name), os.path.join(os.getcwd(), "templates/" + name))
    print(session.get('type'))
    idt = gettype(session.get('type'))[0]
    idu = getid(request.environ['REMOTE_ADDR'])[0]

    con = mysql.connect()
    cursor = con.cursor()
    q = "INSERT INTO user_type VALUES (" + str(idu) + "," + str(idt) + ",'" + str(name) + "')"
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
        "SELECT type.idtype,type.label,count(type.idtype) AS nb FROM type,textvote WHERE type.idtype = textvote.type GROUP BY type.idtype,type.label ORDER BY  nb  DESC LIMIT 4;")
    data = cursor.fetchall()
    cursor.close()
    con.close()
    return json.dumps(data)

    return getrandomdataint()


@app.route('/1data')
def getrandomintjson():
    return getrandomdataint()


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


def getid(ip):
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT userip FROM user WHERE userip ='" + ip + "'")
    data = cursor.fetchone()

    if data is None:

        cursor.execute("INSERT INTO user (userip) VALUES ('" + ip + "')")
        cursor.close()
        con.commit()
        cursor = con.cursor()
        cursor.execute("SELECT iduser FROM user WHERE userip ='" + ip + "'")
        data = cursor.fetchone()
        cursor.close()
        con.close()
        return data
    else:
        query = "SELECT iduser FROM user WHERE userip ='" + ip + "'"
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run()
