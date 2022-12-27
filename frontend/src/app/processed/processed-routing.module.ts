import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProcessedPage } from './processed.page';

const routes: Routes = [
  {
    path: '',
    component: ProcessedPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ProcessedPageRoutingModule {}
