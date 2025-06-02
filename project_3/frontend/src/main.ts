// import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
// import { AppModule } from './app/app.module';
//
// platformBrowserDynamic()
//   .bootstrapModule(AppModule, {
//   ngZoneEventCoalescing: true,
// })
//   .catch(err => console.error(err));

import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

fetch('/assets/config/app.config.js')
  .then(resp => resp.text())
  .then(jsContent => {
    eval(jsContent);
    platformBrowserDynamic()
      .bootstrapModule(AppModule, {
        ngZoneEventCoalescing: true,
      })
      .catch(err => console.error(err));
  });
