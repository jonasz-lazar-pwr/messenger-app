import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-login-page',
  standalone: false,
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent {
  email: string | undefined;
  password: string | undefined;

  constructor(private authService: AuthService) {}

  onSubmit(form: NgForm) {
    if (form.valid) {
      const { email, password } = form.value;

      // Wywołanie metody logowania z AuthService (np. za pomocą JWT, OAuth, itp.)
      this.authService.login(email, password).subscribe(response => {
        console.log('User logged in:', response);
        // Możesz np. przekierować użytkownika na stronę główną lub dashboard
      }, error => {
        console.error('Login error:', error);
      });
    }
  }
}
