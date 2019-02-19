import optparse
from indexer.elasticsearch_connector import ElasticsearchConnector
from indexer.parser import HTMLparser
import glob
import os

parser = optparse.OptionParser()

parser.add_option('-i', '--input', dest="input", help="Input path", required=True)

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

connector = ElasticsearchConnector()

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
            parsed_content = HTMLparser(f.read())
            connector.store(
                title = parsed_content['title'],
                content = parsed_content['content'],
                url = files_info[filename]['url'],
                blog = filepath.split(os.path.sep)[-3]
            )
        print('Created files: {}'.format(i), end='\r')
        i+=1

