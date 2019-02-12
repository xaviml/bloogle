import scrapy
from .base_spider import BaseSpider

class SteemitSpider(BaseSpider):
    name = 'steemit'

    def get_initial_url(self):
        return [
            'https://steemit.com'
        ]
        
    def get_next_links(self):
        return [
            'a[href*="https://steemit.com/"]',
            'a[href^="/"]'
        ]

    def get_file_name(self, url):
        return url.split("/")[-1].split("?")[0]

    def get_domain(self):
        return "https://steemit.com"

    def is_relevant(self, url, body_selector):
        title = body_selector.css('div.PostFull__header h1.entry-title')
        return len(title) == 1

    def is_dynamic(self):
        return False

    def allow_leaving_domain(self):
        return False

    def get_timer(self):
        return 0
