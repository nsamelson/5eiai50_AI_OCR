import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ProcessedPageRoutingModule } from './processed-routing.module';

import { ProcessedPage } from './processed.page';
import { PdfViewerModule } from 'ng2-pdf-viewer';


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ProcessedPageRoutingModule,
    PdfViewerModule,
  ],
  declarations: [ProcessedPage]
})
export class ProcessedPageModule {}
