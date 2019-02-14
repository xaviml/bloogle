from .simple_base_spider import SimpleBaseSpider

class TechCrunchSpider(SimpleBaseSpider):
    name = 'techcrunch'

    def get_file_name(self, url):
        return url.split("/")[-2]

    def get_domain(self):
        return 'https://techcrunch.com/'