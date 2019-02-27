# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json

class BlooglePipeline(object):

    def __init__(self):
        self.links = dict()
        self.counter = 0

    def open_spider(self, spider):
        # Open the links.json
        # Creating the directory for the crawler
        self.output_dir = os.path.join(spider.path, spider.name, 'pages', '')
        self.links_file_path = os.path.join(spider.path,  spider.name, 'links.json')
        os.makedirs(self.output_dir, exist_ok=True)

        if os.path.exists(self.links_file_path):
            self.links = self.read_json(self.links_file_path)

    def process_item(self, item, spider):
        filename = self.output_dir + item['filename']
        
        # Save the content of the HTML
        if not (spider.is_refreshing() and item['url'] in self.links):
            with open(filename, 'w', encoding="utf-8") as f:
                f.write(item['body'])
        
            self.links[item['url']] = {
                'filename' : item['filename'],
                'links' : item['links']
            }
            self.counter += 1
            if spider.is_refreshing():
                msg = '[{}] New pages crawled: {}'
            else:
                msg = '[{}] Pages crawled: {}'
            print(msg.format(spider.name, self.counter))

        return item

    def close_spider(self, spider):
        # write on the file and save the links
        self.write_json(self.links_file_path)

    def read_json(self, path):
        out = None
        with open(self.links_file_path, encoding="utf-8") as f:
            out = json.load(f)
        return out

    def write_json(self, path):
        with open(self.links_file_path, 'w', encoding="utf-8") as fp:
            json.dump(self.links, fp)