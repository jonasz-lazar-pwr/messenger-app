import { Injectable } from '@angular/core';
import { OidcSecurityService } from 'angular-auth-oidc-client';
import { catchError, Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { jwtDecode } from 'jwt-decode';
import { runtimeEnv } from '../../environments/runtime-env';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(
    private oidcSecurityService: OidcSecurityService,
    private http: HttpClient
  ) {}

  // Decodes the ID token and extracts the user's "sub" (unique identifier)
  getUserSub(): string | null {
    const idToken = this.getIdToken();
    if (!idToken) return null;

    try {
      const decoded: any = jwtDecode(idToken);
      return decoded.sub || null;
    } catch (e) {
      console.error('Failed to decode ID token', e);
      return null;
    }
  }

  // Returns true if the user is authenticated (based on presence of id_token)
  isAuthenticated(): boolean {
    return !!this.getTokenFromSessionStorage('id_token');
  }

  // Retrieves the ID token from sessionStorage
  getIdToken(): string | null {
    return this.getTokenFromSessionStorage('id_token');
  }


  // Reads either id_token or access_token from OIDC sessionStorage entry
  private getTokenFromSessionStorage(tokenType: 'id_token' | 'access_token'): string | null {
    const storageKeys = Object.keys(sessionStorage);
    const oidcKey = storageKeys.find(key => key.startsWith('0-'));

    if (!oidcKey) return null;

    try {
      const storedData = JSON.parse(sessionStorage.getItem(oidcKey) || '{}');
      return storedData.authnResult?.[tokenType] || null;
    } catch (error) {
      console.error(`Error parsing sessionStorage data for ${tokenType}:`, error);
      return null;
    }
  }

  // Sends a POST request to backend to register a user (only called once after login)
  registerUser(): Observable<boolean> {
    return this.http.post('/api/users/register', null).pipe(
      map(() => true),
      catchError(error => {
        console.error('User registration failed:', error);
        return of(false);
      })
    );
  }

  // Handles the OIDC login callback and returns whether the user is authenticated
  handleAuthCallback$(): Observable<boolean> {
    return this.oidcSecurityService.checkAuth().pipe(
      map(({ isAuthenticated }) => {
        return isAuthenticated;
      })
    );
  }

  // Starts the OIDC login redirect flow
  login(): void {
    this.oidcSecurityService.authorize();
  }

  // Clears sessionStorage and logs out the user from Cognito
  logout(): void {
    if (window.sessionStorage) {
      window.sessionStorage.clear();
    }
    this.oidcSecurityService.logoff();

    // Redirect after logout
    window.location.href = `${runtimeEnv.cognitoLogoutUrl}?client_id=${runtimeEnv.clientId}&logout_uri=${runtimeEnv.postLogoutRedirectUri}`;
  }
}
