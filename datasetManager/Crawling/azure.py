import http.client, urllib.request, urllib.parse, urllib.error, base64 ,os

headers = {
    # Request headers
    "Ocp-Apim-Subscription-Key": '{'+str(os.environ["BING"])+'}',
}

params = urllib.parse.urlencode({
    # Request parameters
    'q': 'microsoft',
    'count': '10',
    'offset': '0',
    'mkt': 'en-us',
    'safeSearch': 'Strict',
    'size': 'Large'
})

try:
    conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')

    conn.request("GET", "https://api.cognitive.microsoft.com/bing/v7.0/images/search" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print(e)



"""
--- TITLE WITHIN QUIZZ
--- internal server error score



"""