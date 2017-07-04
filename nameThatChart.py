import os, binascii
from flask import Flask, request, session, render_template, send_file
from flaskext.mysql import MySQL
import imagePrep as pics
from random import randint

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


@app.route('/temp')
def temp():
    return render_template('temp.html')


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

    cursor.execute("select iduser from multiplevote where iduser="+str(idu[0])+" and idimage ="+str(idm[0])+"")
    data = cursor.fetchone()

    if data is None:
        final = "INSERT INTO multiplevote (iduser,idimage,idtype) VALUES (" + str(idu[0]) + "," + str(idm[0]) + "," + str(
        idt[0]) + ")"
    else:
        final = "update multiplevote set idtype ="+str(idt[0])+" where iduser="+str(idu[0])+" and idimage ="+str(idm[0])
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


@app.route('/maj')
def maj():
    imgs = pics.getimgs("/home/theo/PycharmProjects/NameThatChart/static/assets/img/datasets/")
    con = mysql.connect()
    cursor = con.cursor()

    for i in range(0, len(imgs)):
        path = imgs[i].replace("/home/theo/PycharmProjects/NameThatChart/static/", "")
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


if __name__ == '__main__':
    app.run()
