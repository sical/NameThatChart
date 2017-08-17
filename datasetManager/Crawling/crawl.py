import codecs
import argparse
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
    # merge("google")
    # getgoogle()
    # getwiki()
    if not os.path.isfile("cart.json") and FLAGS.d == "cart.json":
        cartesian()

    if FLAGS.w == "google":
        getgoogle()
    elif FLAGS.w == "block":
        getblock()
    elif FLAGS.w == "wikipedia":
        getwiki()
    if (FLAGS.merge):
        merge(FLAGS.w)


def getblock():
    info = filetoarray()
    result = {}
    data = parsej()

    for line in info:
        print('\x1b[0;30;44m' + line + '\x1b[0m' + "\n", flush=True)
        print("", flush=True)
        for val in data:
            if line.lower() in val.description.lower() and line not in result.keys():
                result[line] = val.getcompleteurl()
                print('\x1b[6;30;42m' + "Added ! " + '\x1b[0m' + "\n", flush=True)
                print(" ", flush=True)
        print("NEXT", flush=True)

    write_json("block", result)


def merge(name):

    js = getjsonfiles(os.path.join(os.getcwd(),os.path.realpath("../dataset/JsonCrawl/" + name + '.json')))

    data = {}
    null = []
    info = {}

    for file in js:

        if name in file:
            with open(file) as data_file:

                info = json.load(data_file)

                for key in info.keys():
                    if key not in data:
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


def filetoarray():
    result = []
    with open(FLAGS.d, "r") as data_file:
        result = json.load(data_file)
    return result


def getwiki():
    info = filetoarray()
    wiki = {}
    nb = 0
    total = len(info)
    for row in info:
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

    write_json("Wiki", wiki)


def getgoogle():
    info = filetoarray()
    temp = {}
    googleres = {}
    nb = 0
    total = len(info)

    for row in info:
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
    path = os.path.join(os.getcwd(), os.path.realpath("../dataset/JsonCrawl/" + name + '.json'))
    if os.path.exists(path):
        jsons = getjsonfiles(os.getcwd())
        i = 0
        for row in jsons:
            if name in row:
                i += 1
        name += "_" + str(i)
        path = os.path.join(os.getcwd(), os.path.realpath("../dataset/JsonCrawl/" + name + '.json'))
    with open(path, 'wb') as f:
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
    js = getjsonfiles(FLAGS.json_path)
    result = []
    print("Parsing JSON ...")
    for file in js:
        with open(file) as data_file:

            data = json.load(data_file)

            for key in data['blocks'].keys():
                if data['blocks'][key]['description'] is not None and data['blocks'][key]['description'] not in result:
                    result.append(View(data['blocks'][key]['userId'], data['blocks'][key]['description'],
                                       key, data['blocks'][key]['thumbnail']))

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

    data.append(prefix)
    data.append(term)
    data.append(suffix)
    result = list(itertools.product(*data))
    fin = []
    for row in result:
        if row[0] == "" and row[2] == "" and row[1] != "":
            name = row[1]
        elif row[0] == "":
            name = row[1] + " " + row[2]
        elif row[2] == "":
            name = row[0] + " " + row[1]
        else:
            name = row[0] + " " + row[1] + " " + row[2]
        fin.append(name)

    with open("cart" + '.json', 'wb') as f:
        json.dump(fin, codecs.getwriter('utf-8')(f), ensure_ascii=False)

    return fin


def getnames():
    with open("../dataset/Actualdata/FinalGoogle.json", "r") as data_file:
        data = json.load(data_file)
        result = data.keys()
        with open("names" + '.json', 'wb') as f:
            json.dump(list(result), codecs.getwriter('utf-8')(f), ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--w', type=str, default='wikipedia',
                        help='Select name to crawl')
    parser.add_argument('--d', type=str, default='cart.json',
                        help='Select name dataset')
    parser.add_argument('--json_path', type=str, default="/home/theo/Documents/temp/api",
                        help='Select name Json (block) location')
    parser.add_argument('--merge', type=bool, default=False,
                        help='Merge results from given name (see --w) ')
    FLAGS, unparsed = parser.parse_known_args()
    main()
