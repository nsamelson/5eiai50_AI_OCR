import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ImportedPageRoutingModule } from './imported-routing.module';

import { ImportedPage } from './imported.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ImportedPageRoutingModule
  ],
  declarations: [ImportedPage]
})
export class ImportedPageModule {}
