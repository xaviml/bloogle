import requests
from elasticsearch_dsl import connections
from elasticsearch import Elasticsearch
from elasticsearch import helpers as h
from indexer.post import Post
from elasticsearch_dsl import Search

def isPostOnline(url):
    r = requests.get(url)
    return  r.status_code >= 200 and r.status_code < 400, r.status_code

def deletePost(url):
    s = Search(index='blog').query('match', _id=url)
    response = s.delete()
    return response

client = Elasticsearch()
connections.create_connection(hosts=['localhost'], port=9200)

search = Search(using=client).params(request_timeout=999999) # search all blogs

# Count search results
total = search.count()
print('total indexed blogs', total)

i = 0
deletedBlogs = 0
#for post in search.scan():
for d_post in h.scan(client, scroll=u'24h'):
        post = d_post['_source']
        url = post['url']
        isOnline, httpCode = isPostOnline(url)
        if not isOnline:
                deletePost(url)
                deletedBlogs += 1
                print('code', httpCode, 'deleted:', url)
        if i % 1000 == 0:
                print('i = ', i)
        i+=1


print('deletedBlogs', deletedBlogs)