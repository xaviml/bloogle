import scrapy
from scrapy.crawler import CrawlerProcess
from bloogle_bot.spiders.wired_spider import WiredSpider
from bloogle_bot.spiders.medium_spider import MediumSpider
from bloogle_bot.spiders.steemit_spider import SteemitSpider
from bloogle_bot.spiders.gizmodo_spider import GizmodoSpider
from bloogle_bot.spiders.theverge_spider import TheVergeSpider
from bloogle_bot.spiders.techcrunch_spider import TechCrunchSpider
import optparse

parser = optparse.OptionParser()

parser.add_option('-o', '--output',
    action="store", dest="output",
    help="output path", default="data")

options, args = parser.parse_args()

process = CrawlerProcess()
process.crawl(WiredSpider, options.output)
process.crawl(MediumSpider, options.output)
process.crawl(SteemitSpider, options.output)
process.crawl(GizmodoSpider, options.output)
process.crawl(TheVergeSpider, options.output)
process.crawl(TechCrunchSpider, options.output)
process.start() # the script will block here until all crawling jobs are finished