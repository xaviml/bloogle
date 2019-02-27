import { Component, Input, Output, OnChanges, SimpleChange } from '@angular/core';
import { EventEmitter } from '@angular/core';
import { PagerService } from 'src/app/services/pager.service';

@Component({
  selector: 'app-paginator',
  templateUrl: './paginator.component.html',
  styleUrls: ['./paginator.component.scss']
})
export class PaginatorComponent implements OnChanges {
  @Input() numResults: number;
  @Input() resultsPerPage: number;
  @Output() pageClicked: EventEmitter<number> = new EventEmitter();

  numPages: number[];
  pager: any = {};
  constructor(public pagerService: PagerService) {
  }
  ngOnChanges({ numResultsChanges, resultsPerPageChanges }:
    { numResultsChanges: SimpleChange, resultsPerPageChanges: SimpleChange }): void {
    if (numResultsChanges && numResultsChanges.currentValue) {
      this.numResults = numResultsChanges.currentValue;
    }
    if (resultsPerPageChanges && resultsPerPageChanges.currentValue) {
      this.resultsPerPage = resultsPerPageChanges.currentValue;
    }
    if (this.numResults !== null && this.resultsPerPage !== null) {
      this.numPages = Array(Math.ceil(this.numResults / this.resultsPerPage)).fill(0).map((x, i) => i);
      this.setPage(0, false);
    }
  }
  setPage(page: number, emit: boolean) {
    // get pager object from service
    this.pager = this.pagerService.getPager(this.numResults, page);

    if (emit) {
      this.pageClicked.emit(page);
      window.scroll(0, 0);
    }
  }
}
