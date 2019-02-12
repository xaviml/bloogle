from .base_spider import BaseSpider

class WiredSpider(BaseSpider):
    name = "wired"

    def get_initial_url(self):
        return ['https://www.wired.com/author/wired-staff/page/1/',
                'https://www.wired.com/author/wired-staff/page/689/']

    def get_next_links(self):
        return ['li.archive-item-component a.archive-item-component__link',
                'a[href^="https://www.wired.com/story/"]',
                'li.pagination-component__caret--right > a[href]'] 

    def get_file_name(self, url):
        return url.split("/")[-2]

    def get_domain(self):
        return "https://www.wired.com"
        
    def is_relevant(self, url, body_selector):
        if not url.startswith(self.get_domain()):
            return False
        if url.startswith('https://www.wired.com/story/'):
            return True
        title = body_selector.css('header > h1')
        return len(title) == 2

    def is_dynamic(self):
        return False

    def get_timer(self):
        return 0