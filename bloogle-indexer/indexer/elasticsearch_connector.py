from elasticsearch import Elasticsearch

class ElasticsearchConnector():

    def __init__(self):
        self.es = Elasticsearch()
        self.__configure__()
        

    def __configure__(self):

        # Follow this post to configure: https://towardsdatascience.com/getting-started-with-elasticsearch-in-python-c3598e718380
        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        # self.es.indices.create(index='bloogle', ignore = 400)
        pass

    # Create methods to store data
    # Guidelines:
    #   * index: 'bloogle'
    #   * _type: post
    #   * id: don't especify, so it will be created automatically
    #   * Attributes to be stored:
    #       * title: Indexable
    #       * content: Indexable
    #       * URL: non-indexable
    #       * blog: indexable {medium, wired, etc...}
    #       * title: Indexable