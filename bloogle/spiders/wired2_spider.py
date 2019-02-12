import scrapy


class Wired2Spide(scrapy.Spider):
    name = "wired2"
    start_urls = [
        'https://www.wired.com/author/wired-staff/page/1/'
    ]

    def parse(self, response):
        if response.url:
            pass
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

