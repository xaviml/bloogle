# bloogle-indexer: Module responsible to index the data

## Run
To run the *run.py*, a flag *-i* must be in the options indicating the path of the folder with all the crawled data. Recommended command line:
```
python run.py -i ../data/
```

## Debug
In case that you want to run this module again, you must remove the content from elasticsearch:
```
curl -x DELETE http://localhost:9200/_all
```