from PIL import Image
import os, os.path
import argparse


def main():
    # convert2gray("jpg", "/home/theo/Dropbox/TER/Images/bar chart/", "/home/theo/temp/la/")
    # resize("jpg", "/home/theo/Dropbox/TER/Images/bar chart/", "/home/theo/temp/lo/", 100, 100)
    clear(FLAGS.inp, FLAGS.size)


def convert2gray(ext, path, output):
    output = checkpath(output)
    to = "L"

    if ext == "png":
        to = "LA"

    i = 0
    for imgp in getimgs(path):
        img = Image.open(imgp).convert(
            to)  # convert the image to a 'L' or 'LA' format (both are black and white format)
        img.save(output + str(i) + "." + ext)
        i = i + 1


def getimgs(path):
    imgs = []
    valid_images = [".jpg", ".gif", ".png", ".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]  # reverse search of '.' and send it. If no '.', send empty String
        if ext.lower() not in valid_images:
            continue
        imgs.append(os.path.join(path, f))
    return imgs


def resize(ext, path, outputDir, width, height):
    size = width, height
    outputDir = checkpath(outputDir)

    i = 0
    for imgp in getimgs(path):
        img = Image.open(imgp).resize(size, Image.ANTIALIAS)  # Resize the image
        img.save(outputDir + str(i) + "." + ext)
        i += 1


def resize2gray(ext, path, outputDir, width, height):
    size = width, height
    outputDir = checkpath(outputDir)
    to = "L"

    if ext == "png":
        to = "LA"

    i = 0
    for imgp in getimgs(path):
        # Resize the image, then
        # convert the image to a 'L' or 'LA' format (both are black and white format).
        img = Image.open(imgp).resize(size, Image.ANTIALIAS).convert(to)
        img.save(outputDir + str(i) + "." + ext)
        i += 1


def checkpath(path):
    if not (path.endswith("/")):
        path += "/"
    return path


def clear(path, size):
    imgs = getimgs(path)
    print(str(len(imgs)))
    for img in imgs:
        try:
            a = Image.open(img)
            width, height = a.size
            if width < size or height < size:
                os.remove(img)

        except Exception as e:
            print(e)
            os.remove(img)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inp', type=str, default='/home/theo/Dropbox/TER/Images/bar chart/',
                        help='Directory for storing input data')
    parser.add_argument('--out', type=str, default='/home/theo/temp/la/',
                        help='Directory for storing output data')
    parser.add_argument('--ext', type=str, default='jpg',
                        help='Extention for output data')
    parser.add_argument('--size', type=int, default=100,
                        help='Size for output data')
    FLAGS, unparsed = parser.parse_known_args()
    main()
