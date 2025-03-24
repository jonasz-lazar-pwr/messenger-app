import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConversationService {

  constructor(private http: HttpClient) {}

  // Retrieves a list of all conversations for the authenticated user
  getConversations(): Observable<any[]> {
    return this.http.get<any[]>('/api/conversations');
  }
}
