import scrapy
from .base_spider import BaseSpider

class SimpleBaseSpider(BaseSpider):

    def get_initial_url(self):
        return [
            self.get_domain()
        ]
        
    def get_next_links(self):
        return [
            'a[href^="'+self.get_domain()+'"]',
            'a[href^="/"]'
        ]

    def is_relevant(self, url, body_selector):
        ldjsonList = body_selector.css('script[type="application/ld+json"]')
        for ldjson in ldjsonList.getall():
            if '"@type":"NewsArticle"' in ldjson:
                return True
        return False
        
    def is_dynamic(self):
        return False

    def allow_leaving_domain(self):
        return False

    def get_timer(self):
        return 0
