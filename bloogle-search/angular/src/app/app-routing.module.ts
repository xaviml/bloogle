import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainSearchComponent } from './components/main-search/main-search.component';
import { SearchInputComponent } from './components/search-input/search-input.component';
import { routeNames } from './route-names';


const routes: Routes = [
  { path: '', component: MainSearchComponent, pathMatch: 'full' },
  { path: routeNames.SEARCH, component: SearchInputComponent, pathMatch: 'full' },
  { path: '**', component: MainSearchComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
