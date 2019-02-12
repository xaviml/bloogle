import scrapy
from .base_spider import BaseSpider

class MediumSpider(BaseSpider):
    name = 'medium'

    def get_initial_url(self):
        return ['https://medium.com/s/story/lifes-little-regularizers-6052b0cc43ac',
        'https://medium.com/s/the-upgrade/8-reasons-why-apple-wont-buy-netflix-f52733f4666',
        'https://medium.com/the-new-york-times/how-to-be-creative-ecfca5ab7518',
        'https://medium.com/s/office-politics/3-disasters-to-avoid-when-youre-growing-a-startup-1df4de6221ac',
        'https://medium.com/s/radical-spirits/how-tucker-carlson-saved-my-life-a25946836300',
        'https://medium.com/s/story/i-am-a-little-too-fat-im-a-little-too-generous-i-think-i-know-why-e97cd25b7eeb',
        'https://medium.com/@shl/reflecting-on-my-failure-to-build-a-billion-dollar-company-b0c31d7db0e7']

    def get_next_links(self):
        return ['div.streamItem a.link']


    def get_file_name(self, url):
        return url.split("/")[-1]

    def get_domain(self):
        return "https://medium.com"

    def is_relevant(self, url, body):
        return True

    def is_dynamic(self):
        return True

    def get_timer(self):
        return 3
