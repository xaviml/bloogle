from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text


class Post(Document):
    title = Text(fields={'raw': Keyword()}, analyzer='english', boost=3)
    content = Text(analyzer='english', boost=2)
    rawContent = Text(boost=2)
    author = Text(fields={'raw': Keyword()}, analyzer='english', boost=1)
    datePublished = Date()
    dateModified = Date()
    url = Text()

    class Index:
        name = 'blog'
        settings = {
            "number_of_shards": 2,
            "number_of_replicas": 0,
            "index": {
                "similarity": {
                    "default": {
                        "type": "BM25",
                        "b": 0.75,
                        "k1": 1.2
                    }
                }
            },
            "analysis": {
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english"
                    },
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 20
                    }
                },
                "analyzer": {
                    "english_exact": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase"
                        ]
                    },
                    "english": {
                        "tokenizer": "standard",
                        "filter": [
                            "english_possessive_stemmer",
                            "lowercase",
                            "english_stop",
                            "english_stemmer"
                        ]
                    },
                    "autocomplete": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter"
                        ]
                    }
                }
            }
        }
