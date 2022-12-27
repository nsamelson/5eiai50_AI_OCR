import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ImportedPage } from './imported.page';

const routes: Routes = [
  {
    path: '',
    component: ImportedPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ImportedPageRoutingModule {}
