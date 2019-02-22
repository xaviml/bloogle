import optparse
from elasticsearch_dsl import connections
from indexer.parser import HTMLparser
from indexer.post import Post
import glob
import os

parser = optparse.OptionParser()

parser.add_option('-i', '--input', dest="input", help="Input path", default='data')

options, args = parser.parse_args()
#options.input -> to access the data folder


def read_links(filepath):
    output = {}
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            output[l[0]] = {
                'url': l[1],
                'links': l[2:]
            }
    return output  

def inits():
    #Post.init()
    pass

connections.create_connection(hosts=['localhost'], port=9200)
inits()

# for loop through htmls file, calling the parser and elasticsearch
path = os.path.join(options.input, '*')
folders = glob.glob(path)
i = 1
for folder in folders:
    linkspath =  os.path.join(folder, 'links.txt')
    path = os.path.join(folder, 'page', '*')
    filepaths = glob.glob(path)
    files_info = read_links(linkspath)
    for filepath in filepaths:
        with open(filepath, 'r', encoding="utf-8") as f:
            filename = filepath.split(os.path.sep)[-1]
            blogName = filepath.split(os.path.sep)[-3]
            post = HTMLparser(f.read(), blogName)
            post.save()
        print('Created files: {}'.format(i), end='\r')
        i+=1

