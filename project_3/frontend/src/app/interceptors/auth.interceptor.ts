import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { runtimeEnv } from '../../environments/runtime-env';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const idToken = this.authService.getIdToken();

    // Only modify requests targeting the backend API (e.g., api/*)
    if (req.url.startsWith('api') && idToken) {
      const apiReq = req.clone({
        // Prefix the request with the full backend API base URL
        url: `${runtimeEnv.apiUrl}${req.url}`,
        // Attach the Authorization header with the user's ID token
        setHeaders: {
          Authorization: `Bearer ${idToken}`
        }
      });

      return next.handle(apiReq);
    }

    // For non-API requests or missing token, pass the request through unchanged
    return next.handle(req);
  }
}
