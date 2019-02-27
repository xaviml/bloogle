import { Injectable } from '@angular/core';
import { Client } from 'elasticsearch-browser';
import { Post } from '../model/post';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { from } from 'rxjs';
import { ElasticSearchResult, ElasticSearchRequest, ElasticDateRange } from '../model/elastic-search';

@Injectable({
  providedIn: 'root'
})
export class ElasticsearchService {
  public readonly DEFAULT_NUM_PAGES = 10;
  private client: Client;
  private readonly _index = 'blog';
  private readonly _type = 'doc';

  private query(q: string, num: number, fromNum: number, gte?: ElasticDateRange) {
    const query: ElasticSearchRequest = {
      'query': {
        'bool': {
          'must': [
            {
              'multi_match': {
                'query': q,
                'fields': [
                  'content',
                  'publishDate',
                  'publishModified',
                  'author'
                ]
              }
            }
          ]
        }
      },
      'highlight': {
        'pre_tags': [
          '<strong>'],
        'post_tags': [
          '</strong>'],
        'fields': {
          'content': {
          }
        }
      },
      'from': fromNum,
      'size': num
    };
    if (gte) {
      query.query.bool.must.push({
        'range': {
          'datePublished': {
            'gte': gte
          }
        }
      });
    }

    return query;
  }

  constructor() {
    this.client = new Client({
      host: 'http://localhost:9200',
      log: 'trace',
    });
  }



  search(query, page = 0, gte?: ElasticDateRange): Observable<QueryResult> {
    const p: Promise<any> = this.client.search({
      index: this._index,
      type: this._type,
      body: this.query(query, this.DEFAULT_NUM_PAGES, page * this.DEFAULT_NUM_PAGES, gte),
    });
    return from(p).pipe(map(this.mapES));
  }
  searchOne(query): Observable<QueryResult> {
    const p: Promise<ElasticSearchResult> = this.client.search({
      index: this._index,
      type: this._type,
      body: this.query(query, 1, 0),
    });
    return from(p).pipe(map(this.mapES));
  }

  private mapES(r: ElasticSearchResult): QueryResult {
    const queryResult = new QueryResult();
    queryResult.time = r.took;
    queryResult.numResults = r.hits.total;
    queryResult.posts = r.hits.hits.map(item => {
      const p = item._source;
      p.content = item.highlight.content.join('...').concat('...');
      return p;
    });
    return queryResult;
  }
}

export class QueryResult {
  time: number;
  numResults: number;
  posts: Post[];
}
