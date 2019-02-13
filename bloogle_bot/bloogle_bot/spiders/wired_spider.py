from .simple_base_spider import SimpleBaseSpider

class WiredSpider(SimpleBaseSpider):
    name = "wired"

    def get_domain(self):
        return "https://www.wired.com"