import argparse
import json
import os
import requests
import re
import wget

from possibleview import View


def main():
    print('aaa')
    parsej()


def getthumb():
    js = getjsonfiles(os.path.join(os.getcwd(), "json_dataset"))
    result = []
    for i in range(0, len(js)):
        print(js[i])
        data = json.load(open(js[i]))
        keylist = []
        for key in data['blocks'].keys():
            if len(key) == 7:
                keylist.append(key)

        print("laaalaaa")
        for i in range(0, len(keylist)):
            if (data['blocks'][keylist[i]]['description'] is not None) and (
                        data['blocks'][keylist[i]]['thumbnail'] is not None):
                result.append(
                    View(data['blocks'][keylist[i]]['userId'],
                         data['blocks'][keylist[i]]['description'].replace("/", ""), keylist[i],
                         data['blocks'][keylist[i]]['thumbnail']))
    print('aaa')
    return savethumb(result)


def savethumb(views):
    # wget.download("https://gist.githubusercontent.com/michalskop/5684941/raw/6fded20522514e13df47b1d88b06676cc6a7d65e/thumbnail.png", "/home/theo/img.png")
    for view in views:
        print(str(len(view.thumb)))
        if (len(view.thumb) > 0):
            q = os.path.join(os.getcwd(), "static/assets/img/datasets/thumbnails/" + view.getthumb())
            print(q + "\n")
            print(view.thumb)
            try:
                wget.download(view.thumb, q)
            except Exception as e:
                print("Error")
                print(e)

    return views


def followurl(views):
    result = []
    for view in views:
        print(view.getcompleteurl())
        f = requests.get(view.getcompleteurl())
        m = re.search('(raw[A-z0-9/]+index.html)', f.text)

        if m:
            found = m.group(1)
            view.url = view.getcompleteurl() + found
            result.append(view)
    print(result[0].url)
    return getit(result)


def getit(views):
    for view in views:
        file = wget.download(view.url, os.path.join(os.getcwd(), "temporald3/" + view.getlocation()))
    return views


def parsej():
    # js =getjsonfiles(os.path.join(os.getcwd(),"jsondata"))
    # for i in range (0,len(js)):
    with open(os.path.join(os.getcwd(), "temp_jsondata/d3.svg.line.json")) as data_file:
        data = json.load(data_file)
        keylist = []
        for key in data['blocks'].keys():
            if len(key) == 7:
                keylist.append(key)
        result = []
        for i in range(0, len(keylist)):
            if data['blocks'][keylist[i]]['description'] is not None:
                result.append(
                    View(data['blocks'][keylist[i]]['userId'], data['blocks'][keylist[i]]['description'], keylist[i],
                         data['blocks'][keylist[i]]['thumbnail']))
        return followurl(result)


def getjsonfiles(path):
    imgs = []
    valid_images = [".json"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]  # reverse search of '.' and send it. If no '.', send empty String
        if ext.lower() not in valid_images:
            continue
        imgs.append(os.path.join(path, f))
    return imgs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inp', type=str, default='/home/theo/Dropbox/TER/Images/bar chart/',
                        help='Directory for storing input data')

    FLAGS, unparsed = parser.parse_known_args()
    main()
