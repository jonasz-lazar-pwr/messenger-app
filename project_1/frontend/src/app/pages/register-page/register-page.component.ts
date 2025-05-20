import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { AuthService} from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: false,
  templateUrl: './register-page.component.html',
  styleUrls: ['./register-page.component.css']
})
export class RegisterPageComponent {
  firstName: string | undefined;
  lastName: string | undefined;
  email: string | undefined;
  password: string | undefined;

  constructor(private authService: AuthService) {}

  onSubmit(form: NgForm) {
    if (form.valid) {
      const { firstName, lastName, email, password } = form.value;

      // Wywołanie metody rejestracji z AuthService (Interceptor zajmie się resztą)
      this.authService.register(firstName, lastName, email, password)
        .subscribe(response => {
          console.log('User registered:', response);
        }, error => {
          console.error('Registration error:', error);
        });
    }
  }
}
