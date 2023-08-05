import requests


def translate(word, key, fromkey, doctype='json'):
    if doctype not in "xml json jsonp".split():
        raise Exception("Doctype Error")
    url = "http://fanyi.youdao.com/openapi.do?keyfrom={0}&key={1}&type=data&doctype={2}&version=1.1&q={3}"
    url = url.format(fromkey, key, doctype, word)

    try:
        response = requests.get(url).json()
    except Exception as e:
        raise e

    return response


def tword(word):
    key = '1415423309'
    fromkey = 'steamrep'
    doctype = 'json'

    response = translate(word, key, fromkey, doctype)

    if 'basic' in response.keys():
        print ('\n'.join(response['basic']['explains']))
    else:
        print ("No explain")

def test():
    print("Hello world")