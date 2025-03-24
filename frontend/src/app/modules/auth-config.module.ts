import { NgModule } from '@angular/core';
import { AuthModule } from 'angular-auth-oidc-client';
import { environment } from '../../environments/environment';

@NgModule({
  imports: [AuthModule.forRoot({
    config: {
      ...environment.cognito
    }
  })],
  exports: [AuthModule],
})
export class AuthConfigModule {}

// silentRenew: true,
// useRefreshToken: true,
// renewTimeBeforeTokenExpiresInSeconds: 30,
