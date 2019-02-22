import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SearchInputComponent } from './components/search-input/search-input.component';

const routes: Routes = [
  { path: '', component: SearchInputComponent, pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
