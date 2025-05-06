import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MessageService {
  constructor(private http: HttpClient) {}

  // Retrieves all messages for a given conversation
  getMessages(conversationId: number): Observable<any[]> {
    return this.http.get<any[]>(`/api/conversations/${conversationId}/messages`);
  }

  // Sends a text message to the specified conversation
  sendTextMessage(conversationId: number, content: string): Observable<any> {
    return this.http.post('/api/messages', {
      conversation_id: conversationId,
      content
    });
  }

  // Sends a media file (e.g., image) to the specified conversation
  sendMediaMessage(conversationId: number, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('conversation_id', conversationId.toString());
    formData.append('file', file);

    return this.http.post('/api/messages/media', formData);
  }
}
