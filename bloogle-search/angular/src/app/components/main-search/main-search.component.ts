import { ElasticsearchService, QueryResult } from './../../services/elasticsearch.service';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { routeNames } from 'src/app/route-names';
import { Location } from '@angular/common';
@Component({
  selector: 'app-main-search',
  templateUrl: './main-search.component.html',
  styleUrls: ['./main-search.component.scss']
})
export class MainSearchComponent implements OnInit {
  query: string;
  constructor(private router: Router,
    private location: Location,
    private es: ElasticsearchService) {
      this.location.go('');
    }

  ngOnInit() {
  }

  lucky() {
    this.es.searchOne(this.query).subscribe((queryResult: QueryResult) => {
      if (queryResult.numResults === 0) { // no results
        this.router.navigate([routeNames.SEARCH], { queryParams: { q: this.query, lucky: true } });
      } else { // success
        window.location.href = queryResult.posts[0].url;
      }
    });
  }

  search() {
    this.router.navigate([routeNames.SEARCH], { queryParams: { q: this.query } });
  }

}
