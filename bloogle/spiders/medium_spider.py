import scrapy
from .base_spider import BaseSpider

class MediumSpider(BaseSpider):
    name = 'medium'

    def get_initial_url(self):
        return [
            'https://medium.com/'
        ]
    def get_next_links(self):
        return [
            'a[href*="https://medium.com/"]'
        ]


    def get_file_name(self, url):
        return url.split("/")[-1].split("?")[0]

    def get_domain(self):
        return "https://medium.com"

    def is_relevant(self, url, body_selector):
        ldjsonList = body_selector.css('script[type="application/ld+json"]')
        return len(ldjsonList) == 1 and '"@type":"NewsArticle"' in ldjsonList.xpath('//script/text()')[0].get()
        

    def is_dynamic(self):
        return False

    def allow_leaving_domain(self):
        return False

    def get_timer(self):
        return 0
