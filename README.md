![logo](https://github.com/xaviml/bloogle/raw/master/bloogle-search/src/assets/bloogle.png)
#### Blog post content search engine
Information retrieval systems have revolutionized the way people interact with the internet. They are tools with a wide array of uses which give rise to the need for web search engines that are spe- cialised for specific use cases. In this [paper](https://github.com/xaviml/bloogle/raw/master/paper.pdf), we describe a new blog post search engine and its architecture, starting with data acquisi- tion and followed by data processing and storage. We combined these modules into a single web application where a user is able to query for blog posts in a standard or advanced way. Finally, we discuss the evaluation of the system with collected validation data and discuss our system performance using offline metrics.

## Set up
To run this, you need python >= 3.6.x and install the requirements:
```
pip install -r requirements.txt
```

In addition, [elasticsearch](https://www.elastic.co/downloads/elasticsearch) must be installed and running in http://localhost:9200.

Add the next lines on elasticsearch.yml:
~~~
http.cors.enabled : true
http.cors.allow-origin: "*"
http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers: X-Requested-With,X-Auth-Token,Content-Type,Content-Length
http.cors.allow-credentials: true
~~~

Apart from following this set up instructions, you can follow the submodules instructions if you want to run them all.

## Run
If everything is installed, you can follow the next steps. First, we need to collect some data from the web.

~~~
cd bloogle-bot
python run.py -o ../data
cd ..
~~~

This will create a data directory and will start crawling pages from: Medium, Wired, Gizmodo, Techcrunch, The Verge, Steemit and Buzzfeed. If you want to refresh the repository, you can run the same command and it will detect the automatically the crawled posts and just crawl for new ones.

Now we can run the indexer, it will create the index with Elasticsearch using the data we crawled

~~~
cd bloogle-indexer
python run.py -i ../data
cd ..
~~~

Finally, once we have the inverted indexes created from different parts of the web, we can run the search engine built with Angular.

~~~
cd bloogle-search
ng serve
~~~

Voilà! You can test it and see that it works!
