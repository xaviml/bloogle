import scrapy
from .base_spider import BaseSpider

class MediumSpider(BaseSpider):
    name = 'wired'

    def get_initial_url(self):
        return ['https://www.wired.com/story/monkeys-with-superpower-eyes-could-help-cure-color-blindness/',
        'https://www.wired.com/story/airbnb-hotel-hybrids-more-homey-comfort-less-risk/',
        'https://www.wired.com/story/amazon-aurora-self-driving-roundup/',
        'https://www.wired.com/story/government-shutdown-cybersecurity-recovery/'
        ]

    def get_next_links(self):
        return ['ul.we-recommend-component__items a[href*="/story/"]',
                'div.sponsored-stories-component ul.sponsored-stories-component__items a.recommendation-item-component__link',
                'ul.paywall a[href]',
                'div.wrapper-cards li.card-component__description a[href]']

    def get_file_name(self, url):
        return url.split("/")[-2]

    def get_domain(self):
        return "https://www.wired.com"
