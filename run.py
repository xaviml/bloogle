import scrapy
from scrapy.crawler import CrawlerProcess
from bloogle.spiders.wired_spider import WiredSpider
from bloogle.spiders.medium_spider import MediumSpider
from bloogle.spiders.steemit_spider import SteemitSpider

process = CrawlerProcess()
process.crawl(WiredSpider)
process.crawl(MediumSpider)
process.crawl(SteemitSpider)
process.start() # the script will block here until all crawling jobs are finished