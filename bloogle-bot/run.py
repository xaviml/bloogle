import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from blooglebot.spiders.wired_spider import WiredSpider
from blooglebot.spiders.medium_spider import MediumSpider
from blooglebot.spiders.steemit_spider import SteemitSpider
from blooglebot.spiders.gizmodo_spider import GizmodoSpider
from blooglebot.spiders.theverge_spider import TheVergeSpider
from blooglebot.spiders.techcrunch_spider import TechCrunchSpider
from blooglebot.spiders.buzzfeed_spider import BuzzfeedSpider
import optparse
import os
import json
from datetime import datetime

parser = optparse.OptionParser()

parser.add_option('-o', '--output',
    action="store", dest="output",
    help="output path", default="data")

options, args = parser.parse_args()

metafilename = os.path.join(options.output, 'meta.json')
meta = None
if os.path.exists(metafilename):
    with open(metafilename, encoding="utf-8") as f:
        meta = json.load(f)

os.environ['SCRAPY_SETTINGS_MODULE'] = 'blooglebot.settings'
spiders = [WiredSpider, MediumSpider, SteemitSpider, 
            GizmodoSpider, TheVergeSpider, TechCrunchSpider, BuzzfeedSpider]
process = CrawlerProcess(get_project_settings())
for spider in spiders:
    process.crawl(spider, path=options.output, meta=meta)
process.start() # the script will block here until all crawling jobs are finished

meta = {
    'last_time_crawled': datetime.now().__str__()
}

with open(metafilename, 'w', encoding="utf-8") as fp:
        json.dump(meta, fp)