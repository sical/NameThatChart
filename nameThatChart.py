import csv
import json
import os, binascii
from flask import Flask, request, session, render_template, send_file
from flaskext.mysql import MySQL
import imagePrep as pics
from PIL import Image
from random import randint
import re

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'NameThatChart'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.secret_key = binascii.hexlify(os.urandom(24))


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/multiple')
def temp():
    return render_template('multiple.html')


@app.route('/pie')
def pie():
    return render_template('pietest.html')


@app.route('/textual')
def textual():
    return render_template('textual.html')


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


@app.route('/savetext', methods=['POST'])
def savetext():
    result = request.files['local']
    print(result.filename)
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
    idim = cursor.fetchone()
    idu = getid(request.environ['REMOTE_ADDR'])

    cursor.execute("INSERT INTO textvote VALUES(" + idu + "," + idim[0] + ")")

    cursor.close()
    con.close()

    return


@app.route('/getrandomint')
def getrandomintjson():
    return getrandomdataint()


@app.route('/maj')
def maj():

    imgs = pics.getimgs("./static/assets/img/datasets/")
    con = mysql.connect()
    cursor = con.cursor()

    for i in range(0, len(imgs)):
        path = imgs[i].replace("/static/", "")
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
        con.close()
        return data
    else:
        query = "SELECT iduser FROM user WHERE userip ='" + ip + "'"
        cursor.execute(query)
        data = cursor.fetchone()
        con.close()
        return data


def getrandomdataint():
    nbclasse = randint(3, 13)
    result = {}
    result['res'] = []
    for i in range(0, nbclasse):
        result['res'].append({"key": randint(3, 5000), "name": "foo" + str(i)})
    return json.dumps(result)


def gettype(typename):
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("""SELECT idtype FROM type WHERE lower(label) LIKE %""" + typename + """%""")

    if " " in typename:


        return

"""" json_data = json.dumps(result)
 total = {"total": [json_data]}
 print(total)
 return json.dumps(total)"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run()
