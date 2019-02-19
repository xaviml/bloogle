from readability import Document
from readability.browser import open_in_browser
import webbrowser

# This file is to test 'readability', it processes HTML and clean it giving a title summary and a body summary
# To install the library: pip install readability-lxml
# Once you run this, it will open two tabs on the browser showing the short version and the real version.

data_path = 'data/'
page = 'medium'
number = '5763'
filename = page + '_' + number

url = ''
with open(data_path + page +'/links.txt') as f:
    lines = f.readlines()
    for line in lines:
        l = line.split('\t')
        if l[0] == filename:
            url = l[1]

with open('data/'+ page +'/page/'+ filename) as f:
    doc = Document(f.read())
    result = '<h2>' + doc.short_title() + '</h2><br/>' + doc.summary()
    open_in_browser(result)

webbrowser.open(url)
