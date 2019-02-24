import { ElasticsearchService } from './../../services/elasticsearch.service';
import { Component, OnInit } from '@angular/core';
import { Post } from 'src/app/model/post';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-search-input',
  templateUrl: './search-input.component.html',
  styleUrls: ['./search-input.component.scss']
})
export class SearchInputComponent implements OnInit {
  query: string;
  lucky: boolean;
  posts: Post[];
  showError: boolean;
  constructor(private es: ElasticsearchService,
    private activatedRoute: ActivatedRoute) {
    this.showError = false;
    this.activatedRoute.queryParams.subscribe(queryParamsObj => {
      this.query = queryParamsObj['q'];
      this.lucky = queryParamsObj['lucky'] === 'true';
      if (this.lucky) {
        this.showError = true;
      } else {
        this.doSearch();
      }

    });
  }

  ngOnInit() {
  }

  search() {
    this.doSearch();
  }

  private doSearch() {
    this.showError = false;
    this.es.search(this.query).subscribe(hits => {
      if (hits['hits']) {
        this.posts = hits['hits']['hits'].map(item => item._source);
        this.showError = false;
      } else {
        this.showError = true;
      }
    });
  }
}
