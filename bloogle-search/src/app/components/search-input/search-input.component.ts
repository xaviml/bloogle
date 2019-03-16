import { Post } from './../../model/post';
import { ElasticsearchService, QueryResult } from './../../services/elasticsearch.service';
import { Component, OnInit, AfterViewChecked } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { routeNames } from 'src/app/route-names';
import { ElasticDateRange } from 'src/app/model/elastic-search';
import { ellipsis } from 'ellipsed';
import { MatSnackBar } from '@angular/material';
@Component({
  selector: 'app-search-input',
  templateUrl: './search-input.component.html',
  styleUrls: ['./search-input.component.scss']
})
export class SearchInputComponent implements OnInit, AfterViewChecked {
  ElasticDateRange = ElasticDateRange;
  query: string;
  originalQuery: string;
  lucky: boolean;
  queryResult: QueryResult;
  validation: boolean;
  showError: boolean;
  searching: boolean;
  ellipsisApplied: boolean;
  gte: ElasticDateRange;
  private readonly invertedCommasRe = new RegExp(/"(.*?)"/, 'g');
  private readonly hyphenRe = new RegExp(/-(\w*)/, 'g');
  private readonly plusRe = new RegExp(/\+(\w*)/, 'g');
  constructor(public es: ElasticsearchService,
    private location: Location,
    private activatedRoute: ActivatedRoute,
    private snackBar: MatSnackBar) {
    this.ellipsisApplied = true;
    this.gte = null;
    this.showError = false;
    this.activatedRoute.queryParams.subscribe(queryParamsObj => {
      this.query = queryParamsObj['q'];
      this.lucky = queryParamsObj['lucky'] === 'true';
      this.validation = queryParamsObj['validation'] === 'true';
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
  onChosenRelevancy(isRelevant: boolean, post: Post) {
    console.log(isRelevant, this.query, post);
    this.snackBar.open('Thank you for your feedback!', 'Close', {
      duration: 2000,
    });
  }
  search(query?: string) {
    if (query) {
      this.query = query;
    }
    this.doSearch();
  }
  pageClicked(page) {
    this.doSearch(page);
  }
  private doSearch(page?: number) {
    this.showError = false;
    if (this.query) {
      const invertedCommasRegexWrapper: RegexWrapper = this.extractMatchingText(this.invertedCommasRe, this.query);
      const plusRegexWrapper: RegexWrapper = this.extractMatchingText(this.plusRe, invertedCommasRegexWrapper.textReplaced);
      const hyphenRegexWrapper: RegexWrapper = this.extractMatchingText(this.hyphenRe, plusRegexWrapper.textReplaced);

      const matches = invertedCommasRegexWrapper.matches.concat(plusRegexWrapper.matches);

      this.searching = true;
      this.originalQuery = this.query;
      this.es.search(
        hyphenRegexWrapper.textReplaced,
        this.query,
        page,
        this.gte,
        matches,
        hyphenRegexWrapper.matches).subscribe((queryResult: QueryResult) => {
          this.queryResult = queryResult;
          if (this.queryResult.numResults === 0) { // no results
            this.showError = true;
          } else {
            this.ellipsisApplied = false;
            this.showError = false;
          }
          this.location.go(`${routeNames.SEARCH}?q=${this.query}&validation=${this.validation}`);
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
      textReplaced: text.replace(re, '').trim(),
      matches: arr
    };
  }
}

interface RegexWrapper {
  valid: boolean;
  textReplaced: string;
  matches: string[];
}
