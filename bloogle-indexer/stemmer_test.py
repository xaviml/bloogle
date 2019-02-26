from elasticsearch_dsl import connections
from elasticsearch import Elasticsearch
from indexer.post import Post

client = Elasticsearch()
connections.create_connection(hosts=['localhost'], port=9200)
Post.init()

Post(
        title= 'title',
        content= 'a beds the tables',
        author= 'author',
        datePublished= '2012-05-04',
        dateModified= '2012-05-04',
        url='url'
    ).save()