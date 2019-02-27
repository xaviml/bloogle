import { ElasticsearchService, QueryResult } from './../../services/elasticsearch.service';
import { Component, OnInit, AfterViewInit, AfterViewChecked } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { routeNames } from 'src/app/route-names';
import { ElasticDateRange } from 'src/app/model/elastic-search';
import { ellipsis } from 'ellipsed';
@Component({
  selector: 'app-search-input',
  templateUrl: './search-input.component.html',
  styleUrls: ['./search-input.component.scss']
})
export class SearchInputComponent implements OnInit, AfterViewChecked {
  ElasticDateRange = ElasticDateRange;
  query: string;
  lucky: boolean;
  queryResult: QueryResult;
  showError: boolean;
  searching: boolean;
  ellipsisApplied: boolean;
  gte: ElasticDateRange;
  private readonly invertedCommasRe = new RegExp(/"(.*?)"/, 'g');
  constructor(public es: ElasticsearchService,
    private location: Location,
    private activatedRoute: ActivatedRoute) {
    this.ellipsisApplied = true;
    this.gte = null;
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
  ngAfterViewChecked(): void {
    if (!this.ellipsisApplied) {
      ellipsis('.content.doesNotHaveHtml', 3);
      this.ellipsisApplied = true;
    }
  }
  search() {
    this.doSearch();
  }
  pageClicked(page) {
    this.doSearch(page);
  }
  private doSearch(page?: number) {
    this.showError = false;
    if (this.query) {
      const regexWrapper: RegexWrapper = this.extractMatchingText(this.invertedCommasRe, this.query);
      console.log('exact', regexWrapper);
      this.searching = true;
      this.es.search(regexWrapper.textReplaced, page, this.gte, regexWrapper.matches).subscribe((queryResult: QueryResult) => {
        if (queryResult.numResults === 0) { // no results
          this.showError = true;
        } else {
          this.ellipsisApplied = false;
          this.queryResult = queryResult;
          this.showError = false;
        }
        this.location.go(`${routeNames.SEARCH}?q=${this.query}`);
        this.searching = false;
      });
    }
  }
  private extractMatchingText(re: RegExp, text: string): RegexWrapper {
    const arr: string[] = [];
    let valid;
    let result;
    do {
      result = re.exec(text);
      if (result) {
        arr[arr.length] = result[1];
      }
      if (valid === undefined) {
        valid = result != null;
      }
    } while (result);
    return <RegexWrapper>{
      valid,
      textReplaced: text.replace(re, ''),
      matches: arr
    };
  }
}

interface RegexWrapper {
  valid: boolean;
  textReplaced: string;
  matches: string[];
}
