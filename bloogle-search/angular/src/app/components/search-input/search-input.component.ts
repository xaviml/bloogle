import { ElasticsearchService, QueryResult } from './../../services/elasticsearch.service';
import { Component, OnInit } from '@angular/core';
import { Post } from 'src/app/model/post';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { routeNames } from 'src/app/route-names';
@Component({
  selector: 'app-search-input',
  templateUrl: './search-input.component.html',
  styleUrls: ['./search-input.component.scss']
})
export class SearchInputComponent implements OnInit {
  query: string;
  lucky: boolean;
  queryResult: QueryResult;
  showError: boolean;
  constructor(private es: ElasticsearchService,
    private location: Location,
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
    if (this.query) {
      this.es.search(this.query).subscribe((queryResult: QueryResult) => {
        if (queryResult.numResults === 0) { // no results
          this.showError = true;
        } else {
          this.queryResult = queryResult;
          this.showError = false;
        }
        this.location.go(`${routeNames.SEARCH}?q=${this.query}`);
      });
    }
  }
}
