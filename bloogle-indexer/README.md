# bloogle-indexer: Module responsible to index the data

## Debugging
In case that you want to run this module again, you must remove the content from elasticsearch:
```
curl -x DELETE http://localhost:9200/_all
```