import argparse
import os
import wget
from PIL import Image
import sys

sys.path.append('../../classes/')
from imagetype import ImgType



def main():
    getimgtypes()


def getimgtypes():
    result = []
    with open(FLAGS.input_file, "r") as file:
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
            if width < FLAGS.min_size:
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
    temp2 = FLAGS.input_file.split('/')
    temp = temp2[len(temp2) - 1].split('.')

    ext2 = str(temp[len(temp) - 1])
    print(ext2)
    print(temp2[len(temp2) - 1][:-len(ext2) - 1])
    path = os.path.join(FLAGS.output_dir, temp2[len(temp2) - 1][:-len(ext2) - 1])
    i = 1
    if os.path.exists(path):
        patht = path + "_" + str(i)
        while os.path.exists(patht):
            i += 1
            patht = path + "_" + str(i)
        path = patht
    os.makedirs(path)
    if not path.endswith("/"):
        path += "/"

    for img in imgs:
        temp = img.url.split('.')

        ext = str(temp[len(temp) - 1])

        q = path + img.type + "_" + str(i) + "." + ext
        try:
            print('\x1b[7;33;40m' + str(i) + '\x1b[0m' + "_""Getting ....  .. ." + img.url + "\n")
            wget.download(img.url, q)
            print('\x1b[6;30;42m' + "Done ! " + '\x1b[0m' + "\n")
            i += 1
            img.path = q
            result.append(img)
        except Exception as e:
            print('\x1b[6;30;41m' + str(e) + '\x1b[0m')

    return clear(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='vis10cat.txt',
                        help='Select input file default : vis10cat.txt ')
    parser.add_argument('--min_size', type=int, default=400,
                        help='Set image size to purge dataset default 400')

    parser.add_argument('--output_dir', type=str, default=str(os.getcwd()),
                        help='Set output dir')
    FLAGS, unparsed = parser.parse_known_args()
    main()
    main()
