import binascii
import datetime
import json
import os
import time
from random import randint

from PIL import Image
from flask import Flask, request, session, render_template
from flask import url_for
from flaskext.mysql import MySQL

import d3jsdownload as dl
import imagePrep as pics
import wget
from flask import send_from_directory

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


@app.route('/nav')
def na():
    return render_template('nav.html')

@app.route('/multiple')
def temp():
    return render_template('multiple.html')


@app.route('/temporary')
def temporary():
    return render_template('temporary.html')


@app.route('/textual')
def textual():
    return render_template('textual.html')


@app.route('/swipes')
def swipes():
    return render_template('swipes.html')


@app.route('/textualimg')
def textualimg():
    return render_template('textualimg.html')


@app.route('/test')
def test():
    return render_template('biovisualize:_Simple_Binary_Tree.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/hybrid')
def hybrid():
    a = randint(0, 100)
    if a > 50:
        return render_template("textual.html")
    else:
        return render_template('textualimg.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/uploadimg')
def uploadimg():
    return render_template('uploadimg.html')


@app.route('/hum')
def hum():
    return render_template('preview/1_7.html')


@app.route('/selectimg')
def selectimg():
    return render_template('selectimg.html')


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


# get data like {"a": 45}
@app.route('/1data')
def getrandomintjson():
    return getrandomdataint()


# get data like {'val1':5 'val2':45}
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

    cursor.execute("SELECT iduser FROM multiplevote WHERE iduser=" + str(idu) + " AND idimage =" + str(idm[0]) + "")
    data = cursor.fetchone()

    if data is None:
        final = "INSERT INTO multiplevote (iduser,idimage,idtype) VALUES (" + str(idu) + "," + str(
            idm[0]) + "," + str(
            idt[0]) + ")"
    else:
        final = "UPDATE multiplevote SET idtype =" + str(idt[0]) + " WHERE iduser=" + str(
            idu) + " AND idimage =" + str(idm[0])
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
    idu = getid(request.environ['REMOTE_ADDR'])
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


@app.route('/savepreview')
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


@app.route('/getnextimg')
def getnextimg():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT imagepath,idimage FROM image WHERE `from` ='json' ORDER BY rand() LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    con.close()
    session['idimg'] = data[1]
    print(data[0])
    return "static/" + str(data[0])


@app.route('/userstats')
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


@app.route('/saveupimg', methods=['POST'])
def saveupimg():
    title = request.form['name']
    url = request.form['url']
    cat = request.form['cat']
    nb = len(pics.getimgs("./static/assets/img/datasets/json/")) + 2

    name = wget.detect_filename(url)
    temp = name.split('.')

    ext = str(temp[len(temp) - 1])

    title = title.replace(" ", "_")
    q = os.path.join(os.getcwd(), "static/assets/img/datasets/json/" + str(nb) + "_" + title + "." + ext)

    wget.download(url, q)
    q = q.replace("/home/theo/PycharmProjects/NameThatChart/static/", "")
    con = mysql.connect()
    cursor = con.cursor()
    query = "INSERT INTO image (imagepath,`from`,title,category) VALUES ('" + q + "','json','" + title + "','" + cat + "')"
    print(query)
    cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()

    return 'ok'


@app.route("/upjsonimg", methods=['POST'])
def upjonimg():
    file = request.files['local']
    filestring = ""
    for line in file:
        print(str(line)[2:][:-3])
        filestring += str(line)[2:][:-3]

    data = json.loads(filestring)
    con = mysql.connect()
    cursor = con.cursor()
    for obj in data:
        print(obj["url"])
        if "url" in obj:

            nb = len(pics.getimgs("./static/assets/img/datasets/json/")) + 2

            name = wget.detect_filename(obj['url'])
            temp = name.split('.')

            ext = str(temp[len(temp) - 1])
            if "title" in obj:
                title = obj["title"].replace(" ", "_")
                q = os.path.join(os.getcwd(), "static/assets/img/datasets/json/" + str(nb) + "_" + title + "." + ext)
            else:
                title = ""
                q = os.path.join(os.getcwd(), "static/assets/img/datasets/json/" + str(nb) + "." + ext)
            wget.download(obj['url'], q)
            q = q.replace("/home/theo/PycharmProjects/NameThatChart/static/", "")

            if 'category' in obj:
                if 'dificulty' in obj:
                    query = "INSERT INTO image (imagepath,`from`,title,category,dificulty) VALUES ('" + q + "','json','" + title + "','" + \
                            obj['category'] + "','" + obj["dificulty"] + "')"
                else:
                    query = "INSERT INTO image (imagepath,`from`,title,category) VALUES ('" + q + "','json','" + title + "','" + \
                            obj['category'] + "')"
            else:
                query = "INSERT INTO image (imagepath,`from`,title) VALUES ('" + q + "','json','" + title + "')"

            cursor.execute(query)
    con.commit()
    cursor.close()
    con.close()

    return 'ok'


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
    return res


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
                if (subi + 1 < len(sub)):
                    subi = subi + 1
                nbsb = nbsb + 1

            elif val[0] == skip[skipi][0]:
                skiptot += (
                               datetime.datetime.strptime(skip[skipi][1],
                                                          "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                                   val[1],
                                   "%Y-%m-%d %H:%M:%S.%f")).total_seconds() * 1000

                if (skipi + 1 < len(skip)):
                    skipi = skipi + 1
                nbsk = nbsk + 1
        else:
            print(nbsb)
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
                if (subi + 1 < len(sub)):
                    subi = subi + 1
                nbsb = 1


            elif val[0] == skip[skipi]:
                skiptot += (
                               datetime.datetime.strptime(skip[skipi][1],
                                                          "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                                   val[1],
                                   "%Y-%m-%d %H:%M:%S.%f")).total_seconds() * 1000
                if (skipi + 1 < len(skip)):
                    skipi = skipi + 1
                nbsk = 1
        if len(subresult) == 0:
            if nbsb > 0:
                subresult.append(subtot / nbsb)

        if nbsk > 0:
            skipresult.append(skiptot / nbsk)

    return subresult, skipresult


@app.route('/saveselect', methods=['POST'])
def saveselect():
    iduser = getid(request.environ['REMOTE_ADDR'])
    idtype = request.form['idtype']
    idimg = request.form['idimage']

    print(str(idtype) + " TYPE")
    print(str(idimg) + "IMAGE")

    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "INSERT INTO selection (idimage,idtype,iduser) VALUES (" + str(idimg) + "," + str(idtype) + "," + str(
            iduser) + ")")

    cursor.close()
    con.commit()
    con.close()

    return 'ok'


@app.route('/getselect')
def getselect():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute(
        "SELECT type.idtype,label FROM sql11185116.textvote INNER JOIN type ON type.idtype = textvote.idtype WHERE type.idtype IS NOT NULL GROUP BY type.idtype,label HAVING count(type.idtype) > 3 ORDER BY rand() LIMIT 1")
    idtype = cursor.fetchone()

    cursor.execute(
        "SELECT imagepath,image.idimage FROM textvote INNER JOIN image ON image.idimage = textvote.idimage WHERE idtype = " + str(
            idtype[0]) + " ORDER BY rand() LIMIT 9")

    imgs = cursor.fetchall()
    cursor.close()
    con.close()
    result = '{' \
             '"name":"' + idtype[1] + '", ' \
                                      '"idtype":"' + str(idtype[0]) + '", ' \
                                                                      '"imgs": ['

    for row in imgs:
        result += '{"path": "' + str(row[0]) + '","id":' + str(row[1]) + '},'

    result = result[:-1]
    result += ']' \
              '}'
    print(result)

    return result


# <------------------ Textual tools ------------------>


@app.route('/getnext')
def getnext():
    con = mysql.connect()
    cursor = con.cursor()
    if (session.get('last') is None):

        cursor.execute("SELECT url,idtype FROM user_type ORDER BY RAND() LIMIT 1")
    else:
        cursor.execute("SELECT url,idtype FROM user_type WHERE NOT idtype='" + str(
            session.get('last')) + "' ORDER BY RAND() LIMIT 1")
    data = cursor.fetchone()

    session['last'] = data[1]
    cursor.close()
    con.close()
    return data[0]


@app.route('/saveimg', methods=['POST'])
def saveimg():
    result = request.files['local']
    img = Image.open(result)
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, img)
    con = mysql.connect()
    cursor = con.cursor()
    nb = len(pics.getimgs("./static/assets/img/datasets/textualsaved/")) + 2
    path = "assets/img/datasets/textualsaved/" + str(nb) + ".jpg"
    print(path)
    bg.save("./static/" + path)

    cursor.execute("INSERT INTO image (imagepath) VALUES ('" + path + "')")
    con.commit()
    query = "SELECT idimage FROM image WHERE imagepath = '" + path + "'"
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
    idu = getid(request.environ['REMOTE_ADDR'])

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
    for i in range(0, len(data)):
        result.append("static/" + str(data[i][0]))

    cursor.close()
    con.close()
    return json.dumps(result)


@app.route('/getfive', )
def getfive():
    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("SELECT imagepath,idimage,max(number),idtype  "
                   "FROM (SELECT image.idimage,imagepath ,count(idtype) AS number,idtype FROM selection INNER JOIN image ON image.idimage = selection.idimage "
                   "GROUP BY image.idimage, idtype) AS temp GROUP BY idimage ORDER BY rand() LIMIT 5")
    data = cursor.fetchall()

    result = "[ "

    for i in range(0, len(data)):
        cursor.execute("SELECT label FROM type WHERE idtype =" + str(data[i][3]))
        temp = cursor.fetchone()[0]
        result += '{' \
                  '"path" : "static/' + str(data[i][0]) + '",' \
                                                          '"label" : "' + temp + '",' \
                                                                                 '"idimage": ' + str(data[i][1]) + ',' \
                                                                                                                   '"idtype": ' + str(
            data[i][3]) + '' \
                          '},'
    result = result[:-1]
    result += " ]"
    cursor.close()
    con.close()
    return result


@app.route('/saveswipe', methods=['POST'])
def saveswipe():
    idimage = request.form["idimage"]
    vote = request.form["vote"]
    idtype = request.form["idtype"]
    iduser = getid(request.environ['REMOTE_ADDR'])


    con = mysql.connect()
    cursor = con.cursor()

    cursor.execute("insert into swipe (idimage,idtype,iduser,vote) values ("+str(idimage)+","+str(idtype)+","+str(iduser)+","+str(to_bool(vote))+")")

    cursor.close()
    con.commit()
    con.close()
    return 'ok'


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


@app.route('/getnextpic')
def getnextpic():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("SELECT imgpath FROM image  WHERE `from` ='json' ORDER BY RAND() LIMIT 1")

    data = cursor.fetchone()

    cursor.close()
    con.close()
    return data[0]


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
        query = "SELECT iduser FROM user WHERE ipuser ='" + ip + "'"
        cursor.execute(query)
        data = cursor.fetchone()
        con.close()
        return data[0]


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


def to_bool(s):
    return 1 if s == 'true' else 0

def gettimes():
    now = datetime.datetime.now()
    timestamp = str(time.mktime(now.timetuple())).replace(".0", "")
    return str(now)[:-3], timestamp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run()
