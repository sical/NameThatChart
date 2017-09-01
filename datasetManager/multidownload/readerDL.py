import argparse
import os
import sys
import json

sys.path.append('../classes/')
from imagetype import ImgType
from dlthread import Downloader


def main():

    if FLAGS.type == 'txt':
        getimgtypestxt(FLAGS.output_dir, FLAGS.input_file)
    else:
        getimgtypesfromjson(FLAGS.output_dir, FLAGS.input_file)

def chunks(l, n):
    return [l[i::n] for i in range(n)]


def getimgtypesfromtxt(path, filename):
    result = []
    nb = 0
    with open(filename) as file:
        for line in file:
            nb += 1
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



def getimgtypesfromjson(path, filename):

    result = []
    nb = 0
    with open(filename) as file:
        data = json.load(file)


        for key in data.keys():
            for row in data[key]:
                nb += 1
                result.append(ImgType(key, row))

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
    parser.add_argument('--input_file', type=str, default='vis10cat.txt',
                        help='Select input file default : vis10cat.txt ')
    parser.add_argument('--output_dir', type=str, default=str(os.getcwd()),
                        help='Set ouput directory (default current)')

    parser.add_argument('--type', type=str, default="txt",
                        help='Set input type default (txt) alt : json')


    FLAGS, unparsed = parser.parse_known_args()
    main()
