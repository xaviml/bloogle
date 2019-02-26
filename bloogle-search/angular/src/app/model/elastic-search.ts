export interface Shards {
  total: number;
  successful: number;
  skipped: number;
  failed: number;
}

export interface Source {
  title: string;
  content: string;
  author: string;
  datePublished: Date;
  dateModified: Date;
  url: string;
}

export interface Highlight {
  content: string[];
}

export interface Hit {
  _index: string;
  _type: string;
  _id: string;
  _score: number;
  _source: Source;
  highlight: Highlight;
}

export interface Hits {
  total: number;
  max_score: number;
  hits: Hit[];
}

export interface ElasticSearchResult {
  took: number;
  timed_out: boolean;
  _shards: Shards;
  hits: Hits;
}
