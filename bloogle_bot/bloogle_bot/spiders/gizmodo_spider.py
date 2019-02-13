from .simple_base_spider import SimpleBaseSpider

class GizmodoSpider(SimpleBaseSpider):
    name = 'gizmodo'

    def get_domain(self):
        return "https://gizmodo.com"