import argparse
import os
import wget
import threading
import sys

from dlthread import Downloader
from imagetype import ImgType
import imagePrep as pics


def main(_):
    return 'ok'


def chunks(l, n):
    return [l[i::n] for i in range(n)]


def getimgtypes(path, filename):
    result = []
    nb =0
    with open(filename + ".txt") as file:
        for line in file:
            nb+=1
            temp = str(line.rstrip()).split("\t")
            result.append(ImgType(temp[0], temp[1]))
    out = os.path.join(os.getcwd(), path)

    li = chunks(result, 5)

    t1 = Downloader(li[0], out, '\x1b[0;30;44m')

    t2 = Downloader(li[1], out, '\x1b[0;30;45m')
    t3 = Downloader(li[3], out, '\x1b[0;30;46m')

    t4 = Downloader(li[4], out, '\x1b[0;30;47m')

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    return nb


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    FLAGS, unparsed = parser.parse_known_args()
    main()
