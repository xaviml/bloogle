import { Injectable } from '@angular/core';
import { Client } from 'elasticsearch-browser';
import { Post } from '../model/post';
import { Observable } from 'rxjs';
import { from } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ElasticsearchService {
  private client: Client;
  private readonly _index = "blog";
  private readonly _type = "doc";
  private queryAllPosts = {
    'query': {
      'match_all': {}
    }
  };
  private query(q) {
    return {
      "query": {
        "multi_match": {
          "query": q,
          "fields": ["content", "publishDate", "publishModified", "author"]
        }
      },
      "from": 0,
      "size": 10
    };
  }

  constructor() {
    this.client = new Client({
      host: 'http://localhost:9200',
      log: 'trace',
    });
  }



  search(query): Observable<Object[]> {
    const p: Promise<any> = this.client.search({
      index: this._index,
      type: this._type,
      body: this.query(query),
      filterPath: ['hits.hits._source']
    });
    return from(p);
  }
}
