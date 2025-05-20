import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RegisterPageComponent } from './register-page.component';
import {RouterModule, Routes} from '@angular/router';
import {FormsModule} from '@angular/forms';

const routes: Routes = [
  { path: '', component: RegisterPageComponent }
];

@NgModule({
  declarations: [RegisterPageComponent],
  imports: [CommonModule, RouterModule.forChild(routes), FormsModule],
  exports: [RegisterPageComponent]
})
export class RegisterPageModule { }
