import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ImportedPageRoutingModule } from './imported-routing.module';

import { ImportedPage } from './imported.page';
// import { HttpClientModule } from '@angular/common/http';
import { PdfViewerModule } from 'ng2-pdf-viewer';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ImportedPageRoutingModule,
    PdfViewerModule,
    // HttpClientModule
  ],
  declarations: [ImportedPage]
})
export class ImportedPageModule {}
