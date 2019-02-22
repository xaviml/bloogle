from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text

class Post(Document):
    title = Text(fields={'raw': Keyword()})
    content = Text(analyzer='snowball')
    author = Text(fields={'raw': Keyword()})
    datePublished = Date()
    dateModified = Date()

    class Index:
        name = 'blog'
        settings = {
          "number_of_shards": 2,
          "number_of_replicas": 0
        }