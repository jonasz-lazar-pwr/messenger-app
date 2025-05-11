import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class MediaLoaderService {

  preloadImage(message: any): Promise<void> {
    return new Promise((resolve) => {
      const img = new Image();
      img.src = message.media_url;
      img.onload = () => {
        message.loading = false;
        resolve();
      };
      img.onerror = () => {
        message.loading = false;
        message.loadFailed = true;
        resolve();
      };
    });
  }
}
