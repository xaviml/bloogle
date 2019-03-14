import requests
from elasticsearch_dsl import connections
from elasticsearch import Elasticsearch
from indexer.post import Post
from elasticsearch_dsl import Search

def isPostOnline(url):
    r = requests.head(url)
    return  r.status_code >= 200 and r.status_code < 300

def deletePost(url):
    s = Search(index='blog').query('match', _id=url)
    response = s.delete()
    return response

client = Elasticsearch()
connections.create_connection(hosts=['localhost'], port=9200)

search = Search(using=client) # search all blogs

# Count search results
total = search.count()
print('total indexed blogs', total)

deletedBlogs = 0
for post in search.scan():
    if not isPostOnline(post.url):
        post.delete()
        deletedBlogs += 1

print('deletedBlogs', deletedBlogs)