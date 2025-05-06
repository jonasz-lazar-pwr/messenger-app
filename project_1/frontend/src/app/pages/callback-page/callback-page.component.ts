import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { of, switchMap } from 'rxjs';

@Component({
  selector: 'app-callback-page',
  standalone: false,
  templateUrl: './callback-page.component.html',
  styleUrl: './callback-page.component.css'
})
export class CallbackPageComponent implements OnInit {
  loading = true;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Handle OIDC login callback and attempt user registration
    this.authService.handleAuthCallback$()
      .pipe(
        switchMap((isAuthenticated) => {
          if (isAuthenticated) {
            // Register user in backend if authenticated
            return this.authService.registerUser();
          } else {
            return of(false);
          }
        })
      )
      .subscribe((success) => {
        this.loading = false;

        // Navigate based on registration result
        if (success) {
          this.router.navigate(['/dashboard']);
        } else {
          this.router.navigate(['/']);
        }
      });
  }
}
