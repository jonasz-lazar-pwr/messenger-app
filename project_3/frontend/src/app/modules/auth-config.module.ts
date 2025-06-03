import { NgModule } from '@angular/core';
import { AuthModule } from 'angular-auth-oidc-client';
import { runtimeEnv } from '../../environments/runtime-env';

@NgModule({
  imports: [AuthModule.forRoot({
    config: {
      authority: runtimeEnv.authority,
      clientId: runtimeEnv.clientId,
      redirectUrl: runtimeEnv.redirectUrl,
      responseType: runtimeEnv.responseType,
      scope: runtimeEnv.scope,
      postLogoutRedirectUri: runtimeEnv.postLogoutRedirectUri
    }
  })],
  exports: [AuthModule],
})
export class AuthConfigModule {}
