import optparse
from elasticsearch_dsl import connections
from indexer.parser import HTMLparser
from indexer.post import Post
import glob
import os
import json

parser = optparse.OptionParser()

parser.add_option('-i', '--input', dest="input", help="Input path", default='data')

options, args = parser.parse_args()
#options.input -> to access the data folder

def read_links(filepath):
    jsonfile = {}
    with open(filepath) as f:
        jsonfile = json.load(f)
    out = {}
    for k,v in jsonfile.items():
        out[v['filename']] = v
        out[v['filename']]['url'] = k
        del out[v['filename']]['filename']
    return out 

def inits():
    #Post.init()
    pass

connections.create_connection(hosts=['localhost'], port=9200)
inits()

path = os.path.join(options.input, 'links.json')
files_info = read_links(path)

# for loop through htmls file, calling the parser and elasticsearch
path = os.path.join(options.input, 'pages', '*')
filepaths = glob.glob(path)
i = 1
for filepath in filepaths:
    with open(filepath, 'r', encoding="utf-8") as f:
        filename = filepath.split(os.path.sep)[-1]
        blogName = filename.split('_')[0]
        post = HTMLparser(f.read(), blogName)
        if post is not None:
            post.save()
    print('Created files: {}'.format(i), end='\r')
    i+=1

