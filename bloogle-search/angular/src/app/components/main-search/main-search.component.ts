import { ElasticsearchService } from './../../services/elasticsearch.service';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { routeNames } from 'src/app/route-names';
import { Post } from 'src/app/model/post';

@Component({
  selector: 'app-main-search',
  templateUrl: './main-search.component.html',
  styleUrls: ['./main-search.component.scss']
})
export class MainSearchComponent implements OnInit {
  query: string;
  constructor(private router: Router,
    private es: ElasticsearchService) { }

  ngOnInit() {
  }

  lucky() {
    this.es.searchOne(this.query).subscribe(hits => {
      if (hits['hits']) {
        const posts: Post[] = hits['hits']['hits'].map(item => item._source);
        window.location.href = posts[0].url;
      } else {
        this.router.navigate([routeNames.SEARCH], { queryParams: { q: this.query, lucky: true } });
      }
    });
  }

  search() {
    this.router.navigate([routeNames.SEARCH], { queryParams: { q: this.query } });
  }

}
