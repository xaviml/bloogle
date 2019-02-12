# bloogle: A Blog Search Engine

## How to create a Spider
There are two options to create an spider:
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

## Set up
To run this, you need python >= 3.6.x and install the requirements:
```
pip install -r requirements.txt
```

### Linux
As an additional step, you need to install chromedriver, for linux follow these commands:
```
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

### Windows
As an additional step, you need to install chromedriver, for windows follow these steps:
* Download: https://chromedriver.storage.googleapis.com/2.41/chromedriver_win32.zip
* 

## Run
```
scrapy crawl my_spider
```

This will start the crawler 'my_spider'. In case the spider extends BaseSpider, then it will create an output folder with the name of the spider and it will contain all the html files.

## Debug
In case of using VSCode, you can run *run.py* and change the crawler you want to execute.