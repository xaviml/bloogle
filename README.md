# bloogle: A Blog Search Engine

## How to create a Spider
There are two option to create an spider:
* Extending from scrapy.Spider and implementing the methods that scrapy.Spider needs
* Extending BaseSpider

## BaseSpider
This is an abstract class that force you to implement the following methods:
* _get_initial_url_: It needs to return a list of starting URLs.
* _get_next_links_: It should return a list of CSS query selector, pointing to an element \<a>
* _get_file_name_: It should returns the name of the file given a URL
* _get_domain_: It needs to return the domain of the website, in case there are relative paths, this domain will be added before sending the request.

 ## Example
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

 ```

 ## Run
 ```
 scrapy crawl my_spider
 ```

 This will start the crawler 'my_spider'. In case the spider extends BaseSpider, then it will create an output folder with the name of the spider and it will contain all the html files.

 ## Debug
 In case of using VSCode, you can run *run.py* in the debug option and change this line to something like:
 ```python
 execute(['scrapy','crawl', 'my_spider'])
 ```