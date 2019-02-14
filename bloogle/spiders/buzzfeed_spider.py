from .simple_base_spider import SimpleBaseSpider

class BuzzfeedSpider(SimpleBaseSpider):
    name = 'buzzfeed'

    def get_domain(self):
        return "https://buzzfeed.com"