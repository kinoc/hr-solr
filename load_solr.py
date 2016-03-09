from bs4 import BeautifulSoup
from sys import argv
import http.client, urllib.parse

script, conv = argv

doc = open(conv).read()
soup = BeautifulSoup(''.join(doc))

conn = http.client.HTTPConnection('localhost', 8983)

#conn.request('POST', '/solr/admin/cores?action=UNLOAD&core=aiml&deleteIndex=true&deleteDataDir=true')
#conn.request('POST', '/solr/admin/cores?action=CREATE&name=aiml&instanceDir=aiml')

docCount = 0

for token in soup('category'):
    if ('srai' not in token.template):
        print('SOLR ', token.pattern.text)

        BODY = """\
[
    {
        "id" : "DOC%s",
        "title" : "%s"
    }
]
""" % (docCount, token.pattern.text)

        docCount = docCount + 1

        headers = {'Content-type': 'application/json'}
        conn.request('POST', '/solr/aiml/update?commit=true', BODY, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        print('DATA', data)

conn.request('POST', '/admin/cores?action=RELOAD&core=query')
