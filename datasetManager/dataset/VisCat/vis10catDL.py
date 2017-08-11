import argparse
import os

from PIL import Image
import sys
sys.path.append('../../classes/')
from imagetype import ImgType


def main():
    return 'ok'

def getimgtypes():
    result = []
    with open("vis16cat.txt") as file:
        for line in file:
            temp = str(line.rstrip()).split("\t")
            result.append(ImgType(temp[0], temp[1]))

    return savethem(result)


def clear(imgs):
    result = []
    for img in imgs:
        try:
            temp = Image.open(img.path)
            width, height = temp.size
            if width < 400:
                os.remove(img.path)
            else:
                result.append(img)
        except Exception as e:
            os.remove(img.path)
            print(e)
    return result


def savethem(imgs):
    i = 0
    result = []
    for img in imgs:
        temp = img.url.split('.')

        ext = str(temp[len(temp) - 1])
        q = os.path.join(os.getcwd(), "static/assets/img/datasets/vis16cat/" + img.type + "_" + str(i) + "." + ext)
        try:
            print('\x1b[7;33;40m' + str(i) + '\x1b[0m' + "_""Getting ....  .. ." + img.url + "\n")
            vaschercher(img.url, q)
            print('\x1b[6;30;42m' + "Done ! " + '\x1b[0m' + "\n")
            i += 1
            img.path = q
            result.append(img)
        except Exception as e:
            print('\x1b[6;30;41m' + str(e) + '\x1b[0m')

    return clear(result)






if __name__ == '__main__':
    main()
