from .base_spider import BaseSpider

class Wired2Spider(BaseSpider):
    name = "wired2"

    def get_initial_url(self):
        return ['https://www.wired.com/author/wired-staff/page/1/']

    def get_next_links(self):
        return ['li.archive-item-component a.archive-item-component__link']

    def get_file_name(self, url):
        return url.split("/")[-2]

    def get_domain(self):
        return "https://www.wired.com"
        
    def is_relevant(self, url, body_selector):
        title = body_selector.css('header.article-main-component__header h1.title')
        return len(title) == 1

    def is_dynamic(self):
        return False

    def get_timer(self):
        return 0