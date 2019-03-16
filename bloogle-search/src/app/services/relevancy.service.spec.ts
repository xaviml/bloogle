import { TestBed, inject } from '@angular/core/testing';

import { RelevancyService } from './relevancy.service';

describe('RelevancyService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [RelevancyService]
    });
  });

  it('should be created', inject([RelevancyService], (service: RelevancyService) => {
    expect(service).toBeTruthy();
  }));
});
