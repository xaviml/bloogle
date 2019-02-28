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
  content?: string[];
  title?: string[];
  pre_tags: string[];
  post_tags: string[];
  fields: Fields;
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
  suggest: SuggestResponse;
}

export interface MultiMatch {
  query: string;
  fields: string[];
}

export enum ElasticDateRange {
  PAST_YEAR = 'now-1y/d',
  PAST_MONTH = 'now-1M/d',
  PAST_WEEK = 'now-1w/d',
}

export interface DatePublished {
  gte: ElasticDateRange;
}

export interface Range {
  datePublished: DatePublished;
}

export interface Must {
  multi_match?: MultiMatch;
  range?: Range;
}

export interface MatchPhrase {
  content?: string;
  title?: string;
}

export interface Should {
  match_phrase: MatchPhrase;
}

export interface MustNot {
  match_phrase: MatchPhrase;
}

export interface Bool {
  must?: Must[];
  should?: Should[];
  must_not?: MustNot[];
}

export interface Query {
  bool: Bool;
}

// tslint:disable-next-line:no-empty-interface
export interface Content {
}
// tslint:disable-next-line:no-empty-interface
export interface Title {
}

export interface Fields {
  content: Content;
  title: Title;
}

export interface Term {
  field: string;
}

export interface Option {
  text: string;
  score: number;
  freq: number;
}

export interface Mytermsuggester {
  text: string;
  term: Term;
  options?: Option[];
}

export interface Suggest {
  mytermsuggester: Mytermsuggester;
}

export interface SuggestResponse {
  mytermsuggester: Mytermsuggester[];
}

export interface ElasticSearchRequest {
  query: Query;
  highlight: Highlight;
  from: number;
  size: number;
  suggest: Suggest;
}
