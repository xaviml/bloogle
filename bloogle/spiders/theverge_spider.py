from .simple_base_spider import SimpleBaseSpider

class TheVergeSpider(SimpleBaseSpider):
    name = 'theverge'

    def get_domain(self):
        return 'https://www.theverge.com'