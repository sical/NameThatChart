import csv
import json
import os, binascii
from flask import Flask, request, session, render_template
from flaskext.mysql import MySQL
import imagePrep as pics
from PIL import Image
from random import randint

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'bb4f44ef9e9757'
app.config['MYSQL_DATABASE_PASSWORD'] = '0cf02e4a'
app.config['MYSQL_DATABASE_DB'] = 'heroku_fe2750702799a19'
app.config['MYSQL_DATABASE_HOST'] = 'eu-cdbr-west-01.cleardb.com'
mysql.init_app(app)

app.secret_key = binascii.hexlify(os.urandom(24))


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
    return render_template(chart + '.html')


@app.route('/preview/<chart>')
def genericprev(chart):
    return render_template("preview/" + chart + '.html')


@app.route('/getinfo')
def getinf():
    return session.get('filename')


@app.route('/preview/finalize')
def prevfin():
    con = mysql.connect()
    cursor = con.cursor()
    q = "INSERT INTO type "
    cursor.execute(q)
    con.commit()
    cursor.close()
    con.close()


@app.route('/presaveviz', methods=['POST'])
def presaveviz():
    file = request.files['local']
    print(file.filename)
    name = request.form['type']
    id = getid(request.environ['REMOTE_ADDR'])[0]
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
    cursor.execute("SELECT url FROM type WHERE url IS NOT NULL ORDER BY RAND() LIMIT 1")
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
    path = "assets/img/datasets/" + str(len(pics.getimgs("./static/assets/img/datasets/")) + 1) + ".jpg"
    bg.save("./static/" + path)

    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("INSERT INTO image (imagepath) VALUES ('" + path + "')")
    con.commit()

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


@app.route('/1data')
def getrandomintjson():
    return getrandomdataint()


@app.route('/firstrow')
def getfirstrow():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT type.idtype,type.label,count(type.idtype) as nb from type,textvote where type.idtype = textvote.type group by type.idtype,type.label order by  nb  desc LIMIT 4;")
    data = cursor.fetchall()
    cursor.close()
    con.close()
    return json.dumps(data)

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
    q = "SELECT idtype FROM type WHERE lower(label) = '""" + typename + "'"
    cursor.execute(q)
    data = cursor.fetchone()
    if data is None:

        if "chart" in typename:
            if "_" in typename or "-" in typename or "." in typename:
                typename = typename.replace("_", "")
                typename = typename.replace("-", "")
                typename = typename.replace(".", "")
            else:
                typename = typename.replace("chart", "_chart")
            q = "SELECT idtype FROM type WHERE lower(label) LIKE '""" + typename + "'"
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
