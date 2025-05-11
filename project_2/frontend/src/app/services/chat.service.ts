import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  constructor(private http: HttpClient) {}

  // Retrieves a list of all chats for the authenticated user
  getChats(): Observable<any[]> {
    return this.http.get<any[]>('/api/chats');
  }

  createChat(targetUserSub: string) {
    return this.http.post<any>(`/api/chats`, { target_user_sub: targetUserSub });
  }

  searchUsers(query: string) {
    return this.http.get<any[]>(`/api/users/search?query=${encodeURIComponent(query)}`);
  }
}
