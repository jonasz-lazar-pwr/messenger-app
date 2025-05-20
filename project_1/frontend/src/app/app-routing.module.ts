import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { path: '', loadChildren: () => import('./pages/landing-page/landing-page.module').then(m => m.LandingPageModule) },
  { path: 'callback', redirectTo: 'callback/', pathMatch: 'full'},
  { path: 'callback/', loadChildren: () => import('./pages/callback-page/callback-page.module').then(m => m.CallbackPageModule) },
  { path: 'dashboard', loadChildren: () => import('./pages/dashboard-page/dashboard-page.module').then(m => m.DashboardPageModule), canActivate: [AuthGuard] },
  { path: '**', redirectTo: '/' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
