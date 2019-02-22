import { ElasticsearchService } from './../../services/elasticsearch.service';
import { Component, OnInit } from '@angular/core';
import { Post } from 'src/app/model/post';

@Component({
  selector: 'app-search-input',
  templateUrl: './search-input.component.html',
  styleUrls: ['./search-input.component.scss']
})
export class SearchInputComponent implements OnInit {
  query: string;
  posts: Post[];
  constructor(private es: ElasticsearchService) { }

  ngOnInit() {
  }
  search() {
    this.es.search(this.query).subscribe(hits => {
      this.posts = hits['hits']['hits'].map(item => item._source);
    });
  }
}
