import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeRoutingModule } from './home-routing.module';
import { HomeComponent } from './home.component';
import { Step1Component } from './step-1/step-1.component';
import { InputFileComponent } from './step-1/input-file/input-file.component';
import { Step2Component } from './step-2/step-2.component';
import { Step3Component } from './step-3/step-3.component';
import { LoaderComponent } from './step-2/loader/loader.component';
import { RefactorResultsComponent } from './step-3/refactor-results/refactor-results.component';
import {FormsModule} from "@angular/forms";


@NgModule({
  declarations: [
    HomeComponent,
    Step1Component,
    InputFileComponent,
    Step2Component,
    Step3Component,
    LoaderComponent,
    RefactorResultsComponent
  ],
  imports: [
    CommonModule,
    HomeRoutingModule,
    FormsModule
  ]
})
export class HomeModule { }
