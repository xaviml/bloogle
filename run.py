import scrapy
from scrapy.crawler import CrawlerProcess
from bloogle.spiders.wired_spider import WiredSpider
from bloogle.spiders.medium_spider import MediumSpider
from bloogle.spiders.steemit_spider import SteemitSpider
from bloogle.spiders.gizmodo_spider import GizmodoSpider
import optparse

parser = optparse.OptionParser()

parser.add_option('-o', '--output',
    action="store", dest="output",
    help="output path", default="output")

options, args = parser.parse_args()

process = CrawlerProcess()
process.crawl(WiredSpider, options.output)
process.crawl(MediumSpider, options.output)
process.crawl(SteemitSpider, options.output)
process.crawl(GizmodoSpider, options.output)
process.start() # the script will block here until all crawling jobs are finished