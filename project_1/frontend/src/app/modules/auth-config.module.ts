import { NgModule } from '@angular/core';
import { AuthModule } from 'angular-auth-oidc-client';
// import { environment } from '../../environments/environment';
import { runtimeEnv } from '../../environments/runtime-env';

@NgModule({
  imports: [AuthModule.forRoot({
    config: {
      authority: runtimeEnv.authority,
      redirectUrl: runtimeEnv.redirectUrl,
      postLogoutRedirectUri: runtimeEnv.postLogoutRedirectUri,
      clientId: runtimeEnv.clientId,
      scope: runtimeEnv.scope,
      responseType: runtimeEnv.responseType
    }
  })],
  exports: [AuthModule],
})
export class AuthConfigModule {}

// silentRenew: true,
// useRefreshToken: true,
// renewTimeBeforeTokenExpiresInSeconds: 30,
