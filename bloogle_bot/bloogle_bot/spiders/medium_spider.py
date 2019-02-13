from .simple_base_spider import SimpleBaseSpider

class MediumSpider(SimpleBaseSpider):
    name = 'medium'

    def get_domain(self):
        return "https://medium.com"