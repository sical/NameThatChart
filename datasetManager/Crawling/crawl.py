import codecs
import itertools
import json
import os
import time
from datetime import datetime
from random import randint
import sys
import requests
import wikipedia
from google import google

sys.path.append('../classes/')
from possibleview import View


def main():
    #merge("google")
    getgoogle()
    #getwiki()

def getblock():
    info, a = cartesian()
    result = {}
    data = parsej()

    for row in info:
        if row[0] == "" and row[2] == "" and row[1] =="":
            pass
        else:
            name = row[0] + " " + row[1] + " " + row[2]

        for val in data:
            if name.lower() in val.description.lower() and name not in result.keys():
                result[name] = val.getcompleteurl()

    for line in a:
        for val in data:
            if line.lower() in val.description.lower() and line not in result.keys():
                result[line] = val.getcompleteurl()

    print(result)


def merge(name):
    js = getjsonfiles(os.path.join(os.getcwd(), "JsonCrawl"))

    data = {}
    null = []
    info = {}

    for file in js:

        if name in file:
            with open(file) as data_file:

                info = json.load(data_file)

                for key in info.keys():
                    if not key in data:
                        if len(info[key]) == 0 and not key in null:
                            null.append(key)
                        elif len(info[key]) > 0:
                            data[key] = info[key]
                    else:
                        if len(info[key]) == 0 and not key in null:
                            null.append(key)
                        elif len(info[key]) > 0:
                            for url in info[key]:
                                if not url in data[key]:
                                    data[key].append(url)
        for row in null:
            if row.lower in info:
                null.remove(row)

    print(null)
    write_json("FinalGoogle", data)


def getwiki():
    info, a = cartesian()
    wiki = {}
    nb = 0
    total = len(a)
    for row in a:
        try:
            print('\x1b[0;30;44m' + row + '\x1b[0m' + "\n")
            print("")
            ny = wikipedia.page(row)
            temp = row.replace(" ", "_").lower() in ny.url.lower()
            if temp or (row.lower().replace("'s", "") in ny.url.lower() \
                                and temp) or (row.lower().replace("'s", "s") in ny.url.lower() and temp) or (
                            row.lower().replace("'", "%27") in ny.url.lower() and temp):
                wiki[row] = ny.url
            silence = randint(2, 10)
            print(ny.url)
            print(" ")
            print("sleeping for " + str(silence) + "seconds")
            print("waiting ... ", end=" ", flush=True)
            y = 10

            for i in range(1, silence):
                if (i / silence) * 100 >= y:
                    print(str(y) + "% ...", end=" ", flush=True)
                    y += 10
                time.sleep(1)
            print("100% ")
            print('\x1b[6;30;42m' + "Done ! " + '\x1b[0m' + "\n")
            print(" ")
            print("---------------(" + str(nb + 1) + "/" + str(total) + ")---------------------")
            nb += 1
        except Exception as e:
            print(e)

    nb = 0
    total = len(info)
    for row in info:
        if row[0] == "" and row[2] == "" and row[1] !="":
            name = row[1]
        elif row[0] == "":
            name = row[1] + " " + row[2]
        elif row[2] == "":
            name = row[0] + " " + row[1]
        else:
            name = row[0] + " " + row[1] + " " + row[2]

        try:
            ny = wikipedia.page(name)
            if row.replace("_", " ").lower() in ny.url.lower():
                wiki[row] = ny.url
            silence = randint(5, 25)

            print(" ")
            print("sleeping for " + str(silence) + "seconds")
            print("waiting ... ", end=" ", flush=True)
            y = 10

            for i in range(1, silence):
                if (i / silence) * 100 >= y:
                    print(str(y) + "% ...", end=" ", flush=True)
                    y += 10
                time.sleep(1)
            print("100% ")
            print('\x1b[6;30;42m' + "Done ! " + '\x1b[0m' + "\n")
            print(" ")
            print("---------------(" + str(nb + 1) + "/" + str(total) + ")---------------------")
            nb += 1
        except Exception as e:
            print(e)
            write_json("Wiki", wiki)


def getgoogle():
    info, a = cartesian()
    temp = {}
    googleres = {}
    nb = 0
    total = len(a)

    for row in a:
        urls = []
        print('\x1b[0;30;44m' + row + '\x1b[0m' + "\n")
        print("")
        try:
            search_results = google.search(str(row) + " data visualization", 2)
            for res in search_results:
                urls.append(res.link)

            temp[row] = urls
            remp, d1 = proof(row, urls)
            googleres[row] = remp

            silence = randint(30, 60)
            datefin = datetime.now()
            dtemp = datefin - d1
            print(dtemp.total_seconds())
            silence -= int(dtemp.total_seconds())
            print(" ")
            print("sleeping for " + str(silence) + " seconds ...")
            print("waiting ... ", end=" ", flush=True)
            y = 10

            for i in range(1, silence):
                if (i / silence) * 100 >= y:
                    print(str(y) + "% ...", end=" ", flush=True)
                    y += 10
                time.sleep(1)
            print("100% ")
            print(" ")
            print('\x1b[6;30;42m' + "Done ! " + '\x1b[0m' + "\n")
            print(" ")
            print("---------------(" + str(nb + 1) + "/" + str(total) + ")---------------------")
            print(" ")
            nb += 1

        except Exception as e:
            print(e)

    write_json("google", googleres)


def write_json(name, data):
    with open(name + '.json', 'wb') as f:
        json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)


def proof(name, urls):
    date1 = datetime.now()
    ok = []
    for url in urls:
        if name.lower() in url.lower() or (name.lower().replace(" ", "_") in url.lower()) or (name.lower().replace(" ",
                                                                                                                   "-") in url.lower() or name.lower().replace(
            " ", "+") in url.lower()) or (name.lower().replace(" ", "+") in url.lower()) or (name.lower().replace("'s",
                                                                                                                  "") in url.lower()) or (
                    name.lower().replace(
                        "'s",
                        "s") in url.lower()) or (name.lower().replace("'", "%27") in url.lower()):
            print('\x1b[6;30;42m' + "Name in url : " + url + '\x1b[0m' + "\n")
            ok.append(str(url))
    for url in urls:
        temp = url.split('_')
        ext = str(temp[0])
        if not str(url) in ok and ext != 'xls':
            try:
                print("Crawling : " + url)
                r = requests.get(url)
                if name.lower() in r.text.lower():
                    ok.append(url)
                    print('\x1b[6;30;42m' + "url added due to crawling :" + str(url) + '\x1b[0m' + "\n")
            except Exception as e:
                print(e)
    return ok, date1


def parsej():
    js = getjsonfiles("/home/theo/Documents/temp/api")
    result = []
    for file in js:
        with open(file) as data_file:

            data = json.load(data_file)

            for key in data['blocks'].keys():
                if data['blocks'][key]['description'] is not None and data['blocks'][key][
                    'description'] not in result:
                    result.append(View(data['blocks'][key]['userId'], data['blocks'][key]['description'],
                                       key,
                                       data['blocks'][key]['thumbnail']))

    print('\x1b[6;30;42m' + "Done ! " + str(len(result)) + " elements" + '\x1b[0m' + "\n")
    return result


def getjsonfiles(path):
    imgs = []
    valid_images = [".json"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(os.path.join(path, f))
    return imgs


def cartesian():
    data = []

    suffix = ["plot", "chart", "diagram", ""]

    prefix = ["", "circular", "radial", "horizontal", "vertical", "stacked", "stack", "variable", "width",
              "grouped",
              "paired", "weighted", "multi", "semi", "nested", "double", "aligned", "diverging", "floating",
              "deviation"]
    term = ["column", "node-link", "dot", "bar", "line", "arc", "scatter", "unit", "bubble", "area", "flow",
            "isotype",
            "two axis", "pictogram", ""]

    a = ['domain specific', 'word tree', 'job voyager', 'Kagi Chart', 'Election map', 'spider', 'fan',
         'map of the market']

    aside = ['Anscombe quartet', 'donut', 'upset', 'pie scatter', 'ring', 'Sparkline', 'Chernoff’s faces',
         'Minard’s map',
         'Sankey diagram', 'table highlight', 'Tukey boxplot', 'self-organized', 'hyperbolic tree', 'decision tree',
         'word cloud', 'bump tree', 'cause/effect', 'hitory flow', 'Kohonen self-organized map', 'stream graph']

    data.append(prefix)
    data.append(term)
    data.append(suffix)
    result = list(itertools.product(*data))
    return result, a


if __name__ == '__main__':
    main()
