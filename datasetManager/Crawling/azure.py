import os
import json
import codecs
import argparse

from py_ms_cognitive import PyMsCognitiveImageSearch

def gotit(search_term):
    urls= []

    search_service = PyMsCognitiveImageSearch(str(os.environ["BING"]), search_term,custom_params={"mkt": "en-US",'safeSearch': 'Strict', 'size': 'Large'})
    result = search_service.search(limit=70, format='json') #1-70



    for images in result:
        urls.append(images.content_url)

    return urls

def main():
    with open(FLAGS.input_file) as data_file:
        data = json.load(data_file)
    res = {}
    for n in data:
        print(n)
        res[n]= gotit(n+" data visualization")

    with open(FLAGS.output_file, 'wb') as f:
        json.dump(res, codecs.getwriter('utf-8')(f), ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, default='names.json',
                        help='Select input file default : names.json ')
    parser.add_argument('--output_file', type=str, default='imagesFromNames.json',
                        help='Set ouput file (default imagesFromNames.json) Be carefull, it writes over files with a same name')