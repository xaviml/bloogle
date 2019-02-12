import scrapy
from scrapy.crawler import CrawlerProcess
from bloogle.spiders.wired_spider import WiredSpider
from bloogle.spiders.medium_spider import MediumSpider

process = CrawlerProcess()
process.crawl(WiredSpider)
# process.crawl(MediumSpider)
process.start() # the script will block here until all crawling jobs are finished