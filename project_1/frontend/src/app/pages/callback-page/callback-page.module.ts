import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { CallbackPageComponent } from './callback-page.component';

const routes: Routes = [
  { path: '', component: CallbackPageComponent },
];

@NgModule({
  declarations: [CallbackPageComponent],
  imports: [CommonModule, RouterModule.forChild(routes)],
  exports: [CallbackPageComponent]
})
export class CallbackPageModule { }
