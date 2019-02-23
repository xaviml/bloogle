import abc
import scrapy
from scrapy import Request
import os
from selenium import webdriver
import time
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
import json
from ..items import BloogleItem
from dateutil.parser import parse
import pytz
import uuid

class BaseSpider(scrapy.Spider, abc.ABC):

    def __init__(self, path='data', meta=None):
        self.path = path
        self.crawled_pages = 0
        self.explored_pages = 0
        self.meta = meta
        self.last_time_crawled = None
        if self.meta is not None:
            self.last_time_crawled = parse(self.meta['last_time_crawled']).replace(tzinfo=pytz.utc)
        super(BaseSpider, self).__init__()

    def start_requests(self):
        urls = self.get_initial_url()
        for url in urls:
            yield self.getRequest(url)
    
    def getRequest(self, url):
        if self.is_dynamic():
            return SeleniumRequest(url=url, callback=self.parse)
        else: 
            return Request(url=url, meta={'dont_merge_cookies': True}, callback=self.parse)

    def parse(self, response):
        if(self.should_stop()):
            raise scrapy.exceptions.CloseSpider('Reached maximum pages: {}'.format(self.crawled_pages))
        url = response.url
        if self.is_dynamic():
            driver = response.request.meta['driver']
            driver.delete_all_cookies()
            time.sleep(self.get_timer())
            body = driver.page_source
        else:
            body = response.body.decode("utf-8")
        body_selector = scrapy.selector.Selector(text=body)

        if self.allow_leaving_domain() and not url.startswith(self.get_domain()):
            return
        
        # Get links from the web page and request again
        links = []
        css_links = self.get_next_links()
        css_function = response.css if not self.is_dynamic() else driver.find_elements_by_css_selector
        for css_link in css_links:
            next_pages = css_function(css_link)
            if next_pages is not None:
                for next_page in next_pages:
                    # In case the link is relative, the domain will be added
                    next_url = next_page.attrib['href'] if not self.is_dynamic() else next_page.get_attribute('href')
                    if next_url.startswith('/'):
                        next_url = self.get_domain() + next_url
                    next_url = next_url.split('?')[0]
                    links.append(next_url)
        
        links = list(set(links))
        if self.is_relevant(url, body_selector):
            
            file_name = self.name + '_' + uuid.uuid4().__str__()

            try:
                soup = BeautifulSoup(body, 'lxml')
                application_json_ld = json.loads(soup.find('script',{'type':'application/ld+json'}).get_text())
            except:
                application_json_ld = None
            
            datePublished = None
            if application_json_ld is not None:
                if 'datePublished' in application_json_ld:
                    datePublished = application_json_ld['datePublished']
                    datePublished = parse(datePublished)
            
            if self.is_refreshing():
                if datePublished is None:
                    return
                elif datePublished < self.last_time_crawled:
                    return

            item = BloogleItem()
            item['filename'] = file_name
            item['body'] = body
            item['url'] = url
            item['links'] = links
            yield item

            self.crawled_pages += 1
            if(self.should_stop()):
                raise scrapy.exceptions.CloseSpider('Reached maximum pages: {}'.format(self.crawled_pages))
        for link in links:
            yield self.getRequest(link)
        self.explored_pages += 1

    def is_refreshing(self):
        return self.meta is not None

    @abc.abstractmethod
    def get_initial_url(self):
        '''
        Returns a list of initial URL to start the requests
        '''
        pass

    @abc.abstractmethod
    def get_next_links(self):
        '''
        Returns a list of css query for the element <a> with href attribute
        '''
        pass

    @abc.abstractmethod
    def get_domain(self):
        '''
        Returns:
            * The domain of the webside is crawling
        '''
        pass

    @abc.abstractmethod
    def is_relevant(self, url, body_selector):
        '''
        Returns:
            * Boolean indicating is a page we want to crawl
        '''
        pass

    @abc.abstractmethod
    def is_dynamic(self):
        '''
        Returns:
            * Boolean indicating whether the page is dynamic or not
        '''
        pass

    @abc.abstractmethod
    def allow_leaving_domain(self):
        '''
        Returns:
            * Boolean indicating whether the crawler is allowed to leave the domain or not
        '''
        pass

    @abc.abstractmethod
    def get_timer(self):
        '''
        Returns:
            * Timer
        '''
        pass

    def should_stop(self):
        '''
        Returns:
            * whether the crawl should stop or not
        '''
        if self.is_refreshing():
            # If the percentage of crawled pages is below 10% and we have more than 99 explored pages, we stop
            return self.explored_pages > 99 and self.crawled_pages * 100 / self.explored_pages < 10
        else:
            return self.crawled_pages >= 10000