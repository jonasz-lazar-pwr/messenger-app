import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class MessageService {
  constructor(private http: HttpClient) {}

  // Retrieves all messages for a given chat
  getMessages(chatId: number): Observable<any[]> {
    return this.http.get<any[]>(`/api/messages/${chatId}/`);
  }

  // Sends a text message to the specified chat
  sendTextMessage(chatId: number, content: string): Observable<any> {
    return this.http.post('/api/messages/text/', {
      chat_id: chatId,
      content
    });
  }

  // Sends a media file (e.g., image) to the specified chat
  sendMediaMessage(chatId: number, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('chat_id', chatId.toString());
    formData.append('media_file', file);

    return this.http.post('/api/messages/media/', formData);
  }
}
