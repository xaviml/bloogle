import abc
import scrapy
import os
from selenium import webdriver
import time
from scrapy_selenium import SeleniumRequest

TIMER = 5

class BaseSpider(scrapy.Spider, abc.ABC):

    def start_requests(self):
        # Creating the directory for the crawler
        self.output_dir = 'output/{}/'.format(self.name)
        os.makedirs(self.output_dir, exist_ok=True)

        urls = self.get_initial_url()
        # Send selenium requests with the start urls
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)
    
    def parse(self, response):
        file_name = self.get_file_name(response.url)
        # We need to think how we will name the files
        filename = self.output_dir + file_name
        driver = response.request.meta['driver']
        driver.delete_all_cookies()

        time.sleep(TIMER)
        
        # Save the content of the HTML
        with open(filename, 'w') as f:
            f.write(driver.page_source)
        self.log('Saved file %s' % filename)
        
        # Get links from the web page and request again
        css_links = self.get_next_links()
        for css_link in css_links:
            next_pages = driver.find_elements_by_css_selector(css_link)
            if next_pages is not None:
                for next_page in next_pages:
                    # In case the link is relative, the domain will be added
                    url = next_page.get_attribute('href')
                    if url.startswith('/'):
                        url = self.get_domain() + url
                    yield SeleniumRequest(url=url, callback=self.parse)

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
    def get_file_name(self, url):
        '''
        Parameters:
            * url: URL request
        Returns:
            * The name of the file for that specific URL
        '''
        pass

    @abc.abstractmethod
    def get_domain(self):
        '''
        Returns:
            * The domain of the webside is crawling
        '''
        pass