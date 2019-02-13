# bloogle_bot: Module that crawls blog sites

## Run
```
scrapy crawl my_spider
```

This will start the crawler 'my_spider'. In case the spider extends BaseSpider, then it will create an output folder with the name of the spider and it will contain all the html files.

## Debug
In case of using VSCode, you can run *run.py* and change the crawler you want to execute.

## How to create a Spider
There are two options to create an spider:
* Extending from scrapy.Spider and implementing the methods that scrapy.Spider needs
* Extending BaseSpider
* Extending SimpleBaseSpider

## BaseSpider
This is an abstract class that force you to implement the following methods:
* _get_initial_url_: It needs to return a list of starting URLs.
* _get_next_links_: It should return a list of CSS query selector, pointing to an element \<a>
* _get_file_name_: It should returns the name of the file given a URL
* _get_domain_: It needs to return the domain of the website, in case there are relative paths, this domain will be added before sending the request.
* *is_relevant*: It returns a boolean indicating is a page we want to crawl.
* *is_dynamic*: It returns a boolean indicating whether the page is dynamic or not.
* *allow_leaving_domain*: It returns a boolean indicating whether the crawler is allowed to leave the domain or not
* *get_timer*: Wait time in case of using selenium (is_dynamic = True)
* *get_max_pages_to_crawled*: It should return the maximum pages to be crawled (Default: 10000)

 ### Example
```python
import scrapy
from .base_spider import BaseSpider

class MySpider(BaseSpider):
    name = 'my_spider'

    def get_initial_url(self):
        return ['http://myspider.com/page1']

    def get_next_links(self):
        return ['div.next a[href]']

    def get_file_name(self, url):
        return url.split("/")[-1]

    def get_domain(self):
        return "https://myspider.com"

    def is_relevant(self, url, body_selector):
        # ... check body_selector
        # If it returns True, it will save the html
        return True
    
    def is_dynamic(self):
        return False
    
    def allow_leaving_domain(self):
        return False

    def get_timer(self):
        return 0
```

## SimpleBaseSpider
This is a much reduced version of BaseSpider. It has most of the methods already implemented and assumes that the webside has an script with type 'application/ld+json' (Google standards). It will crawled the page from the main page and it will only store those files that has '"@type":"NewsArticle"' in the script with type 'application/ld+json'. If needed, other methods can be overwritten.

### Example
```python
import scrapy
from .simple_base_spider import SimpleBaseSpider

class MySpider(SimpleBaseSpider):
    name = 'my_spider'

    def get_domain(self):
        return "https://myspider.com"
```