import os
import json
import codecs

from py_ms_cognitive import PyMsCognitiveImageSearch

def gotit(search_term):
    urls= []

    search_service = PyMsCognitiveImageSearch(str(os.environ["BING"]), search_term,custom_params={"mkt": "en-US",'safeSearch': 'Strict', 'size': 'Large'})
    result = search_service.search(limit=70, format='json') #1-70



    for images in result:
        urls.append(images.content_url)

    return urls


with open("names.json") as data_file:
    data = json.load(data_file)
res = {}
for n in data:
    print(n)
    res[n]= gotit(n+" data visualization")

with open("NamesBing.json", 'wb') as f:
    json.dump(res, codecs.getwriter('utf-8')(f), ensure_ascii=False)
