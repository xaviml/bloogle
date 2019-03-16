import { Injectable } from '@angular/core';
import { Post } from '../model/post';

@Injectable({
  providedIn: 'root'
})
export class RelevancyService {
  private relevancies: Relevancy[] = [];
  constructor() { }

  addRelevancy(query: string, isRelevant: boolean, post: Post) {
    let r: Relevancy = this.getRelevancyIfExists(query);
    if (r) {
      // check if post already exists, if it does update its relevancy, otherwise add it
      let relevantPost: RelevantPost = r.getRelevantPostIfExists(post);
      if (relevantPost) {
        relevantPost.isRelevant = isRelevant;
      } else {
        relevantPost = new RelevantPost(isRelevant, post);
        r.relevantPosts.push(relevantPost);
      }
    } else {
      r = new Relevancy();
      r.query = query;
      r.relevantPosts.push(new RelevantPost(isRelevant, post));
      this.relevancies.push(r);
    }
  }

  saveRelevancies(): void {

  }
  private getRelevancyIfExists(query: string): Relevancy {
    return this.relevancies.find(r => r.query === query);
  }
}

export class Relevancy {
  query: string;
  relevantPosts: RelevantPost[] = [];

  getRelevantPostIfExists(post: Post): RelevantPost {
    return this.relevantPosts.find(r => r.post.url === post.url);
  }
}

export class RelevantPost {
  constructor(public isRelevant: boolean,
    public post: Post) { }
}
