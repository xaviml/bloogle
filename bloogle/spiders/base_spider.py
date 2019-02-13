import abc
import scrapy
from scrapy import Request
import os
from selenium import webdriver
import time
from scrapy_selenium import SeleniumRequest
import os

# to get last-modified date we can:
# -get last-modified response header, it will work if it's dinamic
# -document.lastModified, it should work on static webside
#     document.lastModified
#     "02/12/2019 18:23:43"
# -query google with:
#     https://www.google.com/search?q=inurl:myWebsite&as_qdr=y15
# 
#     and if we get any results, try to get the date:
# 
#     $('.f').textContent.replace('-','').trim()
#     "2 days ago"


class BaseSpider(scrapy.Spider, abc.ABC):

    def __init__(self, path='.'):
        self.path = path
        super(BaseSpider, self).__init__()

    def start_requests(self):
        # Creating the directory for the crawler
        self.output_dir = os.path.join(self.path, self.name, 'page', '')
        self.links_file_path = os.path.join(self.path, self.name, 'links.txt')
        os.makedirs(self.output_dir, exist_ok=True)

        urls = self.get_initial_url()
        for url in urls:
            yield self.getRequest(url)
    
    def getRequest(self, url):
        if self.is_dynamic():
            return SeleniumRequest(url=url, callback=self.parse)
        else: 
            return Request(url=url, callback=self.parse)

    def parse(self, response):
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
                    yield self.getRequest(next_url)
        
        links = list(set(links))
        if self.is_relevant(url, body_selector):
            file_name = self.get_file_name(response.url)
            # We need to think how we will name the files
            filename = self.output_dir + file_name
            
            # Save the content of the HTML
            with open(filename, 'w', encoding="utf-8") as f:
                f.write(body)
            self.log('Saved file %s' % filename)

            # file1 lastmodified main-url url1 url2 url3
            fileInfo = file_name + '\t' + url + '\t' + '\t'.join(links) + '\n'
            
            with open(self.links_file_path, 'a', encoding="utf-8") as f:
                f.write(fileInfo)

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